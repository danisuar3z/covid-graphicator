# -*- coding: utf-8 -*-

# covid_graphicator.py
# Graficador de casos del COVID-19 - Proyecto final para Python ITBA

# Lucas F. Cañas   - Estudiante de Actuario en FCE - UBA - Argentina
# Daniel T. Suárez - Estudiante de Química en FCEN - UBA - Argentina

from input_processer import valid_country, process_countries, correct_date_format, ask_date
from plotter import plot_country, plot_inter, plot_countries, export_excel

from settings import a, h, v, c1, c2, c3, c4, df


def enter():
    input("\nPress ENTER to continue")


def main():

    global df
    global DATA_FILEPATH

    # df = load_data(DATA_FILEPATH)

    while True:

        print(chr(9556) + chr(9552)*(a) + chr(9559))
        print(f"{v}{'COVID DATA GRAPHICATOR':^{a}}{v}")
        print(f"{v}{' Welcome, this program is a graphicator of':<{a}}{v}")
        print(f"{v}{' cases and deaths generated due to the COVID-19':<{a}}{v}")
        print(f"{v}{' pandemic in 2020 (for now)':<{a}}{v}")
        print(f"{chr(9568)}{chr(9552)*(a):<{a}}{chr(9571)}")
        print(f"{v}{' The program has the following options:':{a}}{v}")
        print(f"{v}{' 1- Plot one country':{a}}{v}")
        print(f"{v}{' 2- Plot two countries with intersections':{a}}{v}")
        print(f"{v}{' 3- Plot several countries in logarithmic scale':{a}}{v}")
        print(f"{v}{' 4- Export excel with country ranking by cases':{a}}{v}")
        print(f"{v}{' 5- Exit':{a}}{v}")
        print(chr(9562) + h*a + chr(9565))

        rta = input("- Choose an option: ").strip()

        if rta == "1":
            print("This option works with the input of ONE country only")
            country = False
            while not country:
                country = input("- Enter the country: ")
                country = process_countries(country)

            plot_country(country)
            print("You can now check the plot generated")
            enter()

        elif rta == "2":
            print("This option works with the input of TWO countries only")

            countries = False
            while not countries:
                countries_str = input("- Enter the countries comma (,) delimited: ")
                countries = process_countries(countries_str)

            print("You can leave blank if you don\'t want to specify a date range")
            ini_date = ask_date("- Enter the initial date (Example 2020-05-24): ")
            fin_date = ask_date("- Enter the final date (Example 2020-10-24): ")

            plot_inter(countries, min_date=ini_date, max_date=fin_date)

            print("You can now check the plots generated")
            enter()

        elif rta == "3":
            print("This option works with as many countries you want")

            countries = False
            while not countries:
                countries_str = input("- Enter the countries comma (,) delimited: ")
                countries = process_countries(countries_str)

            print("You can leave blank if you don\'t want to specify a date range")
            ini_date = ask_date("- Enter the initial date (Example 2020-05-24): ")
            fin_date = ask_date("- Enter the final date (Example 2020-10-24): ")

            plot_countries(countries, min_date=ini_date, max_date=fin_date)

            print("You can now check the plots generated")
            enter()

        elif rta == "4":
            export_excel()
            enter()

        elif rta == "5":
            rta = input("- All graphs will be closed. Are you sure? (y/n): ")
            if rta.strip().lower() == "y":

                print("\n" + c1 + h*38 + c2)
                print(f"{v}{'Thanks for using the program':^38}{v}")
                print(f"{v}{'See you next time!':^38}{v}")
                print(c3 + h*38 + c4)
                lucas = "Lucas Ca" + chr(241) + "as"
                dani = "Daniel Su" + chr(225) + "rez"
                sign = lucas + " - " + dani
                print(f"{sign:>40s}")

                break

        else:
            print("Incorrect option")


if __name__ == "__main__":
    main()
