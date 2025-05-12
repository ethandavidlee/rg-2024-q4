import pandas as pd
import datetime
from cross_question_functions import *


def get_gender_counts(df):
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].dropna().value_counts()
        return gender_counts
    else:
        return pd.Series(dtype=int)


def get_age_counts(df):
    if 'Age' in df.columns:
        age_counts = df['Age'].dropna().value_counts()
        return age_counts
    else:
        return pd.Series(dtype=int)


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


def get_region_counts(df):
    if 'US Region' in df.columns:
        region_counts = df['US Region'].dropna().value_counts()
        return region_counts
    if 'UK Region' in df.columns:
        region_counts = df['UK Region'].dropna().value_counts()
        return region_counts
    else:
        return pd.Series(dtype=int)


def get_education_counts(df):
    if 'Education Level' in df.columns:
        education_counts = df['Education Level'].dropna().value_counts()
        return education_counts
    else:
        return pd.Series(dtype=int)


def export_data_to_csv(df, report_folder):
    filename = f'../csv_exports/{report_folder}/demographics.csv'

    write_section_to_csv(get_gender_counts(df).rename_axis('Gender').reset_index(name='Count'), 'Gender', filename, 'w')
    print(get_gender_counts(df))

    write_section_to_csv(get_age_counts(df).rename_axis('Age').reset_index(name='Count'), 'Age', filename, 'a')
    print(get_age_counts(df))

    write_section_to_csv(get_generation_counts(df).rename_axis('Generation').reset_index(name='Count'), 'Generation', filename, 'a')
    print(get_generation_counts(df))

    write_section_to_csv(get_education_counts(df).rename_axis('Education').reset_index(name='Count'), 'Education',
                         filename, 'a')
    print(get_education_counts(df))

    write_section_to_csv(get_region_counts(df).rename_axis('Region').reset_index(name='Count'), 'Region', filename, 'a')
    print(get_region_counts(df))


if __name__ == "__main__":
    # Set variables for analysis
    report_folder = 'rg-2025-q2'

    # Export data to CSV
    import_data_name = f'../csv_exports/{report_folder}/raw-data.csv'
    data_frame = get_df_from_csv(import_data_name)
    export_data_to_csv(data_frame, report_folder)
