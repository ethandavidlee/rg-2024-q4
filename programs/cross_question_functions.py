import pandas as pd
import datetime


def get_df_from_csv(filename):
    """
    Read data from a CSV file into a DataFrame.
    """
    df = pd.read_csv(filename)
    return df


def get_age_list(df):
    if 'Age' in df.columns:
        age = df['Age'].dropna().unique()
        return age
    else:
        return pd.Series(dtype=int)


def get_generations_list():
    return ['Gen Z', 'Millennial', 'Gen X', 'Baby Boomer']


def get_gender_list(df):
    if 'Gender' in df.columns:
        genders = df['Gender'].dropna().unique()
        return genders
    else:
        return pd.Series(dtype=int)


def get_region_list(df):
    if 'US Region' in df.columns:
        regions = df['US Region'].dropna().unique()
        return regions
    elif 'UK Region' in df.columns:
        regions = ['London', 'Northern England', 'Midlands (England)', 'Southern England', 'Scotland', 'Wales',
                   'Northern Ireland']
        return regions
    else:
        return pd.Series(dtype=int)


def get_age(df, respondent):
    if 'Age' in df.columns:
        age = df.loc[respondent, 'Age']
        return age
    else:
        return None


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
    elif 'UK Region' in df.columns:
        subregion = df.loc[respondent, 'UK Region']
        if subregion == 'London':
            region = 'London'
        elif (subregion == 'North East (England' or subregion == 'North West (England)'  # Pollfish mistake with )
              or subregion == 'Yorkshire And The Humber'):
            region = 'Northern England'
        elif subregion == 'West Midlands (England)' or subregion == 'East Midlands (England)':
            region = 'Midlands (England)'
        elif (subregion == 'South East (England)' or subregion == 'East Of England'
              or subregion == 'South West (England)'):
            region = 'Southern England'
        elif subregion == 'Scotland':
            region = 'Scotland'
        elif subregion == 'Wales':
            region = 'Wales'
        elif subregion == 'Northern Ireland':
            region = 'Northern Ireland'
        else:
            region = None
        return region
    else:
        return None


def write_section_to_csv(data, section_name, filename, mode='w'):
    if isinstance(data, pd.DataFrame) and not data.empty:
        with open(filename, mode) as f:
            if mode == 'a':  # Add a newline before the section name only in append mode to avoid leading newlines
                f.write("\n")
            f.write(f"{section_name}\n")  # Write section name to CSV
            data.to_csv(f, index=False, header=True)  # Append data under section name
    else:
        print(f"No {section_name.lower()} to write.")


def export_data_to_csv(overall_data, gender_data, generation_data, age_data, region_data, filename):
    """
    Take the imported data, question, and export all required data to a new CSV with the corresponding filename,
    appending each section of the data to the file.
    """
    write_section_to_csv(overall_data, 'Overall Data', filename, 'w')
    write_section_to_csv(gender_data, 'Gender Data', filename, 'a')
    write_section_to_csv(generation_data, 'Generation Data', filename, 'a')
    write_section_to_csv(age_data, 'Age Data', filename, 'a')
    write_section_to_csv(region_data, 'Region Data', filename, 'a')

