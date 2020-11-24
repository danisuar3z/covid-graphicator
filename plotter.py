import os

import numpy as np
from matplotlib import ticker, pyplot as plt
import pandas as pd

from settings import plt_style, fig_size, df
from input_processer import date_interval

def style(thousand_sep=True):
    """
    """

    plt.style.use(plt_style)
    plt.figure(tight_layout=True, figsize=fig_size)
    plt.xticks(rotation=90)
    if thousand_sep:
        ax = plt.gca()
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ",")))


def find_inter(df2, deaths=False):
    """
    """

    df2["date_ts"] = [date.timestamp() for date in df2.date]

    # Seeking intersections by the change of sign in the subtraction
    if not deaths:
        idx = np.sign(df2.total_cases_y - df2.total_cases_x)
        idx = np.argwhere(np.diff(idx)).flatten()
    else:
        idx = np.sign(df2.total_deaths_y - df2.total_deaths_x)
        idx = np.argwhere(np.diff(idx)).flatten()

    intersections = []
    # Finding the exact graphic intersection
    for i in idx:
        fecha1, fecha2 = df2.date_ts[i], df2.date_ts[i+1]
        if not deaths:
            cases_x1, cases_x2 = df2.total_cases_x[i], df2.total_cases_x[i+1]
            cases_y1, cases_y2 = df2.total_cases_y[i], df2.total_cases_y[i+1]
        else:
            cases_x1, cases_x2 = df2.total_deaths_x[i], df2.total_deaths_x[i+1]
            cases_y1, cases_y2 = df2.total_deaths_y[i], df2.total_deaths_y[i+1]
        # Calculating slopes and intercepts of the lines
        # between the 2 points near the intersection of each country
        # y = m*x + b
        m1 = (cases_x2 - cases_x1) / (fecha2 - fecha1)
        m2 = (cases_y2 - cases_y1) / (fecha2 - fecha1)

        b1 = cases_x1 - m1 * fecha1
        b2 = cases_y1 - m2 * fecha1

        # Calculating intersection with 2 equation system
        # y = y => m1*x+b1 = m2*x+b2
        inter_x = (b2 - b1) / (m1 - m2)
        inter_y = m1*inter_x + b1

        intersections.append((inter_x, inter_y))

    return np.array(intersections)


def plot_country(country):
    """
    """

    global df
    style()
    country_mask = (df.location == country)
    data = df[(country_mask)]
    plt.plot(data.date, data.total_cases, label="Total cases")
    plt.plot(data.date, data.total_deaths, label="Total deaths")
    plt.title(f"Total cases and deaths in {country}")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.legend()
    plt.show(block=False)


def plot_inter(countries, min_date=None, max_date=None):
    """
    """

    global df
    country1_mask = (df.location == countries[0])
    country2_mask = (df.location == countries[1])
    date_mask = date_interval(min_date, max_date)
    country1 = df[(country1_mask) & (date_mask)]
    country2 = df[(country2_mask) & (date_mask)]

    df2 = pd.merge(country1, country2, how="inner", on="date")

    intersections = find_inter(df2)

    # CASES PLOT
    style()
    plt.plot(country1.date, country1.total_cases, label=countries[0])
    plt.plot(country2.date, country2.total_cases, label=countries[1])

    if len(intersections) != 0:
        for inter in intersections:
            try:
                plt.scatter(
                    pd.Timestamp.fromtimestamp(inter[0])+pd.Timedelta(hours=3),
                    inter[1], linewidths=0.8,
                    s=80, zorder=3, facecolors="none", edgecolors="black")
            except ValueError:  # Intersections array may have some NaNs
                pass

    plt.legend()

    plt.title(f"Total cases for {' - '.join(countries)}")
    plt.xlabel("Date")
    plt.ylabel("Cases")

    plt.show(block=False)

    # DEATH PLOT
    deaths_intersections = find_inter(df2, deaths=True)

    style()
    plt.plot(country1.date, country1.total_deaths, label=countries[0])
    plt.plot(country2.date, country2.total_deaths, label=countries[1])

    if len(deaths_intersections) == 0:
        pass
    else:
        for inter in deaths_intersections:
            try:
                plt.scatter(
                    pd.Timestamp.fromtimestamp(inter[0])+pd.Timedelta(hours=3),
                    inter[1], linewidths=0.8,
                    s=80, zorder=3, facecolors="none", edgecolors="black")
            except ValueError:
                pass

    plt.legend()
    plt.title(f"Total deaths for {' - '.join(countries)}")
    plt.xlabel("Date")
    plt.ylabel("Deaths")

    plt.show(block=False)


def plot_countries(countries, min_date=None, max_date=None):
    """
    """

    global df
    style(thousand_sep=False)
    date_mask = date_interval(min_date, max_date)

    for country in countries:
        country_mask = (df.location == country)
        df_country = df[(date_mask) & (country_mask)]

        plt.plot(df_country.date, np.log10(df_country.total_cases), label=country)

    plt.legend(framealpha=0.5, ncol=2)  # ,loc="upper left")
    # plt.ylim([2.7, 7.5])
    # fechas = list(pd.date_range("2020-06-21", "2020-09-21", periods=8))
    # plt.xticks(fechas)
    plt.title("Total cases comparison (log scale)")
    plt.xlabel("Date")
    plt.ylabel("Total cases / $log_{10}$")
    plt.show(block=False)


def export_excel():
    """
    """

    # global df
    df2 = pd.DataFrame(
        data=None, columns=["Country", "Total_cases", "Total_deaths", "Mortality"])
    df2.Country = df.location.unique()

    for country in df2.Country:
        country_filter = (df2.Country == country)
        df2.Total_cases[country_filter] = df.new_cases[df.location == country].sum()
        df2.Total_deaths[country_filter] = df.new_deaths[df.location == country].sum()
        # print(df2.Total_deaths[country_filter].iloc[0]/df2.Total_cases[country_filter].iloc[0])
        df2.Mortality[country_filter] = round(df2.Total_deaths[country_filter].iloc[0]/df2.Total_cases[country_filter].iloc[0], 4)
    df2.sort_values("Total_cases", ascending=False, inplace=True)
    df2["N"] = list(range(len(df2)))
    df2.set_index("N", inplace=True)

    try:
        df2.to_excel("Countries COVID Ranking.xlsx")
        print(f"Created 'Countries COVID Ranking.xlsx' at {os.getcwd()}")
    except ModuleNotFoundError:
        print("Module 'openpyxl' not found!")