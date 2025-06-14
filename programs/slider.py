import pandas as pd
import datetime
import sys
from cross_question_functions import *


def get_df_from_csv(filename):
    """
    Read data from a CSV file into a DataFrame.
    """
    df = pd.read_csv(filename)
    return df


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


def get_generation_counts(df):
    if 'Year Of Birth' not in df.columns and 'Age' not in df.columns:
        return None

    generations = get_generations_list()
    generation_counts = {generation: 0 for generation in generations}
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
    elif 'UK Region' in df.columns:
        subregion_counts = df['UK Region'].dropna().value_counts()
        not_counted = 0
        region_counts = {'London': 0, 'Northern England': 0, 'Midlands (England)': 0, 'Southern England': 0,
                         'Scotland': 0, 'Wales': 0, 'Northern Ireland': 0}
        for subregion, count in subregion_counts.items():
            if subregion == 'London':
                region_counts['London'] += count
            elif (subregion == 'North East (England' or subregion == 'North West (England)'  # Pollfish mistake with )
                  or subregion == 'Yorkshire And The Humber'):
                region_counts['Northern England'] += count
            elif subregion == 'West Midlands (England)' or subregion == 'East Midlands (England)':
                region_counts['Midlands (England)'] += count
            elif (subregion == 'South East (England)' or subregion == 'East Of England'
                  or subregion == 'South West (England)'):
                region_counts['Southern England'] += count
            elif subregion == 'Scotland':
                region_counts['Scotland'] += count
            elif subregion == 'Wales':
                region_counts['Wales'] += count
            elif subregion == 'Northern Ireland':
                region_counts['Northern Ireland'] += count
            else:
                not_counted += count
        print(f'Not included in region counts: {not_counted}')
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


def get_slider_range(df, question):
    if question in df.columns:
        unique_responses = df[question].dropna().unique()
        minimum = min(unique_responses)
        maximum = max(unique_responses)
        return minimum, maximum
    else:
        print('Question not available. Please check that the provided question is valid for this sheet.')
        sys.exit(1)


def calculate_average(slider, count):
    """
    Returns the average rating from a dictionary of slider responses.
    """
    total = 0
    for key, value in slider.items():
        total += key * value
    average = total / count
    return average


def get_overall_data(df, question):
    minimum, maximum = get_slider_range(df, question)
    slider = {rating: 0 for rating in range(minimum, maximum + 1)}
    overall_count = 0

    for _, row in df.iterrows():
        rating = row[question]
        if rating in slider:
            slider[rating] += 1
            overall_count += 1

    # Calculate average
    average = calculate_average(slider, overall_count)

    # Create new dataframe and calculate percentage
    data = []
    for rating, count in slider.items():
        percentage = count / overall_count
        data.append({'All Respondents': 'All Respondents', 'Rating': rating, 'Percentage': percentage})
    data.append({'All Respondents': 'All Respondents', 'Rating': 'Average', 'Percentage': average})

    return pd.DataFrame(data)


def get_gender_data(df, question):
    minimum, maximum = get_slider_range(df, question)
    genders = get_gender_list(df)
    slider_by_gender = {gender: {rating: 0 for rating in range(minimum, maximum + 1)} for gender in genders}
    gender_counts = {gender: 0 for gender in genders}

    for i, row in df.iterrows():
        gender = get_gender(df, i)
        rating = row[question]
        if gender in slider_by_gender and rating in slider_by_gender[gender]:
            slider_by_gender[gender][rating] += 1
            gender_counts[gender] += 1

    # Create new dataframe and calculate percentage
    data = []
    for gender, slider in slider_by_gender.items():
        gender_count = gender_counts[gender]
        average = calculate_average(slider_by_gender[gender], gender_count)

        for rating, count in slider.items():
            percentage = count / gender_count
            data.append({'Gender': gender, 'Rating': rating, 'Percentage': percentage})
        data.append({'Gender': gender, 'Rating': 'Average', 'Percentage': average})

    return pd.DataFrame(data)


def get_generation_data(df, question):
    minimum, maximum = get_slider_range(df, question)
    generations = get_generations_list()
    slider_by_generation = {generation: {rating: 0 for rating in range(minimum, maximum + 1)}
                            for generation in generations}
    generation_counts = {generation: 0 for generation in generations}

    for i, row in df.iterrows():
        generation = get_generation(df, i)
        rating = row[question]
        if generation in slider_by_generation and rating in slider_by_generation[generation]:
            slider_by_generation[generation][rating] += 1
            generation_counts[generation] += 1

    # Create new dataframe and calculate percentage
    data = []
    for generation, slider in slider_by_generation.items():
        generation_count = generation_counts[generation]
        average = calculate_average(slider_by_generation[generation], generation_count)

        for rating, count in slider.items():
            percentage = count / generation_count
            data.append({'Generation': generation, 'Rating': rating, 'Percentage': percentage})
        data.append({'Generation': generation, 'Rating': 'Average', 'Percentage': average})

    return pd.DataFrame(data)


def get_region_data(df, question):
    minimum, maximum = get_slider_range(df, question)
    regions = get_region_list(df)
    slider_by_region = {region: {rating: 0 for rating in range(minimum, maximum + 1)} for region in regions}
    region_counts = {region: 0 for region in regions}

    for i, row in df.iterrows():
        region = get_region(df, i)
        rating = row[question]
        if region in slider_by_region and rating in slider_by_region[region]:
            slider_by_region[region][rating] += 1
            region_counts[region] += 1

    # Create new dataframe and calculate percentage
    data = []
    for region, slider in slider_by_region.items():
        region_count = region_counts[region]
        average = calculate_average(slider_by_region[region], region_count)

        for rating, count in slider.items():
            percentage = count / region_count
            data.append({'Region': region, 'Rating': rating, 'Percentage': percentage})
        data.append({'Region': region, 'Rating': 'Average', 'Percentage': average})

    return pd.DataFrame(data)


def write_section_to_csv(data, section_name, filename, mode='w'):
    if isinstance(data, pd.DataFrame) and not data.empty:
        with open(filename, mode) as f:
            if mode == 'a':  # Add a newline before the section name only in append mode to avoid leading newlines
                f.write("\n")
            f.write(f"{section_name}\n")  # Write section name to CSV
            data.to_csv(f, index=False, header=True)  # Append data under section name
    else:
        print(f"No {section_name.lower()} to write.")


def export_data_to_csv(df, question, filename):
    """
    Take the imported data, question, and export all required data to a new CSV with the corresponding filename,
    appending each section of the data to the file.
    """
    overall_data = get_overall_data(df, question)
    gender_data = get_gender_data(df, question)
    generation_data = get_generation_data(df, question)
    region_data = get_region_data(df, question)

    # Write overall data or print warning
    write_section_to_csv(overall_data, 'Overall Data', filename, 'w')

    # Append other data sections to the CSV with separation
    write_section_to_csv(gender_data, 'Gender Data', filename, 'a')
    write_section_to_csv(generation_data, 'Generation Data', filename, 'a')
    write_section_to_csv(region_data, 'Region Data', filename, 'a')


if __name__ == "__main__":
    import_data_name = '../csv_exports/rg-2024-q4/raw-data.csv'
    data_frame = get_df_from_csv(import_data_name)
    my_question = "How much of a percentage raise do you think is reasonable for employees to receive each year if they don’t get a promotion?"
    export_data_name = 'Question 15.csv'

    export_data_to_csv(data_frame, my_question, export_data_name)
