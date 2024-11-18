import pandas as pd
import datetime


def get_df_from_csv(filename):
    """
    Read data from a CSV file into a DataFrame.
    """
    df = pd.read_csv(filename)
    return df


def get_generation_counts(df):
    if 'Year Of Birth' not in df.columns and 'Age' not in df.columns:
        return None

    generation_counts = {'Gen Z': 0, 'Millennial': 0, 'Gen X': 0, 'Baby Boomer': 0}
    current_year = datetime.datetime.now().year

    if 'Year Of Birth' in df.columns:
        year_counts = df['Year Of Birth'].dropna().value_counts()
        generation_counts = {'Gen Z': 0, 'Millennial': 0, 'Gen X': 0, 'Baby Boomer': 0}
        for year, count in year_counts.items():
            if 1997 <= year <= 2012:
                generation_counts['Gen Z'] += count
            elif 1981 <= year <= 1996:
                generation_counts['Millennial'] += count
            elif 1965 <= year <= 1980:
                generation_counts['Gen X'] += count
            elif 1946 <= year <= 1964:
                generation_counts['Baby Boomer'] += count

    elif 'Age' in df.columns:
        age_counts = df['Age'].dropna().value_counts()
        for age, count in age_counts.items():
            birth_year = current_year - age
            if 1997 <= birth_year <= 2012:
                generation_counts['Gen Z'] += count
            elif 1981 <= birth_year <= 1996:
                generation_counts['Millennial'] += count
            elif 1965 <= birth_year <= 1980:
                generation_counts['Gen X'] += count
            elif 1946 <= birth_year <= 1964:
                generation_counts['Baby Boomer'] += count

    else:
        return None

    return pd.Series(generation_counts)


def get_gender_counts(df):
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].dropna().value_counts()
        return gender_counts
    else:
        return pd.Series(dtype=int)


def get_region_counts(df):
    if 'US Region' in df.columns:
        region_counts = df['US Region'].dropna().value_counts()
        return region_counts
    else:
        return pd.Series(dtype=int)


def get_generation(df, respondent):
    if 'Year Of Birth' not in df.columns and 'Age' not in df.columns:
        return None

    current_year = datetime.datetime.now().year

    if 'Year Of Birth' in df.columns:
        year = df.loc[respondent, 'Year Of Birth']
        if 1997 <= year <= 2012:
            return 'Gen Z'
        elif 1981 <= year <= 1996:
            return 'Millennial'
        elif 1965 <= year <= 1980:
            return 'Gen X'
        elif 1946 <= year <= 1964:
            return 'Baby Boomer'
        else:
            return None

    elif 'Age' in df.columns:
        age = df.loc[respondent, 'Age']
        birth_year = current_year - age
        if 1997 <= birth_year <= 2012:
            return 'Gen Z'
        elif 1981 <= birth_year <= 1996:
            return 'Millennial'
        elif 1965 <= birth_year <= 1980:
            return 'Gen X'
        elif 1946 <= birth_year <= 1964:
            return 'Baby Boomer'
        else:
            return None

    else:
        return None


def get_gender(df, respondent):
    if 'Gender' in df.columns:
        gender = df.loc[respondent, 'Gender']
        return gender
    else:
        return None


def get_region(df, respondent):
    if 'US Region' in df.columns:
        region = df.loc[respondent, 'US Region']
        return region
    else:
        return None


if __name__ == "__main__":
    csv_name = 'raw-data.csv'
    data_frame = get_df_from_csv(csv_name)
    print(get_gender_counts(data_frame))
    print(get_generation_counts(data_frame))
    print(get_region_counts(data_frame))
