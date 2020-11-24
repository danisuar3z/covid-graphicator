import pandas as pd

# Put the path to the data file here
DATA_FILEPATH = "../data/data.csv"

# Width and characters for the program display
a = 49
h = chr(9552)
v = chr(9553)
c1 = chr(9556)
c2 = chr(9559)
c3 = chr(9562)
c4 = chr(9565)

# Plot properties
plt_style = "bmh"  # Check styles with plt.style.available
fig_size = (7, 5)


def load_data(filepath):
    """
    """

    df = pd.read_csv(filepath)
    df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    df = df[["date", "location", "total_cases", "total_deaths",
             "new_cases", "new_deaths"]]
    return df

df = load_data(DATA_FILEPATH)