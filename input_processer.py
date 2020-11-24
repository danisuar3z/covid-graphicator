from settings import df


def valid_country(country):
    """
    """

    global df
    if country in df.location.unique():
        return True
    return False


def process_countries(countries):
    """
    """

    invalid_country_found = False
    if "," in countries:
        countries = countries.split(",")
        for i, country in enumerate(countries):
            countries[i] = country.strip().title()
            if not valid_country(countries[i]):
                invalid_country_found = True
                print(f"* {countries[i]} not found.")

        if invalid_country_found:
            print("** Make sure to enter the country names in english")
            return False

    else:
        countries = countries.strip().title()
        if not valid_country(countries):
            print(f"* {countries} not found")
            print("** Make sure to enter the country names in english")
            return False
    return countries


def correct_date_format(date):
    """
    """

    date = date.strip()

    if date == "":
        return True

    if len(date) != 10:
        return False

    if date[4] != "-" or date[7] != "-":
        return False

    return True


def ask_date(question):
    """
    """

    ok = False
    while not ok:
        date = input(question)
        if correct_date_format(date):
            ok = True
        else:
            print("Incorrect date format. Use YYYY-MM-DD")

    return date


def date_interval(min_date, max_date):
    """
    """

    global df

    if min_date and max_date:
        date_mask = (df.date >= min_date) & (df.date <= max_date)

    elif min_date:
        date_mask = (df.date >= min_date) & (df.date <= df.date.max())

    elif max_date:
        date_mask = (df.date >= df.date.min()) & (df.date <= max_date)

    else:
        date_mask = (df.date >= df.date.min()) & (df.date <= df.date.max())

    return date_mask
