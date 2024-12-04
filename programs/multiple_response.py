import pandas as pd
import datetime
import sys


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


def get_multi_responses(df, question):
    if question not in df.columns:
        return None

    question_responses = set()

    # Identify columns containing responses for the question
    question_columns = [col for col in df.columns if question in col]

    if question_columns:
        # Loop through each column with responses for Q6
        for col in question_columns:
            # Drop empty cells and get unique responses in this column
            unique_responses = df[col].dropna().str.strip().unique()

            # Add each unique response to the list if it's not already present
            for response in unique_responses:
                if response not in question_responses:
                    question_responses.add(response)

    return question_responses


def get_single_multi_response(df, question, respondent):
    # Identify columns containing responses for the question
    question_columns = [col for col in df.columns if question in col]
    responses = []

    if question_columns:
        # Loop through each column with responses for Q6
        for col in question_columns:
            # Drop empty cells and get unique responses in this column
            response = df.loc[respondent, col]
            if not pd.isna(response):
                responses.append(response)
    else:
        print('Question not available. Please check that the provided question is valid for this sheet.')
        sys.exit(1)

    return responses


def get_overall_data(df, question):
    response_options = get_multi_responses(df, question)
    overall_count = 0
    response_data = {response: 0 for response in response_options}

    for i, row in df.iterrows():
        responses = get_single_multi_response(df, question, i)
        for response in responses:
            if response in response_options:
                response_data[response] += 1
        # add to overall count only if the respondent participated in this question
        if responses:
            overall_count += 1

    # Create new dataframe and calculate percentage
    data = []
    for response, count in response_data.items():
        percentage = (count / overall_count)
        data.append({'All respondents': 'All respondents',
                     'Response': response,
                     'Count': count,
                     'Percentage': percentage})

    return pd.DataFrame(data)


def get_generation_data(df, question):
    response_options = get_multi_responses(df, question)
    generation_counts = {generation: 0 for generation in get_generations_list()}
    response_checker = False
    generations = get_generations_list()
    responses_by_generation = {generation: {response: 0 for response in response_options} for generation in generations}

    for i, row in df.iterrows():
        generation = get_generation(df, i)
        responses = get_single_multi_response(df, question, i)
        for response in responses:
            if (generation in responses_by_generation
                    and response in responses_by_generation[generation]):
                responses_by_generation[generation][response] += 1
                response_checker = True
        # add to overall count only if the respondent participated in this question
        if response_checker:
            generation_counts[generation] += 1
            response_checker = False

    # Create new dataframe and calculate percentage
    data = []
    for generation, responses in responses_by_generation.items():
        for response, count in responses.items():
            percentage = (count / generation_counts[generation])
            data.append({'Generation': generation,
                         'Response': response,
                         'Count': count,
                         'Percentage': percentage})

    return pd.DataFrame(data)


def get_gender_data(df, question):
    response_options = get_multi_responses(df, question)
    response_checker = False
    gender_counts = {gender: 0 for gender in get_gender_list(df)}
    genders = get_gender_list(df)
    responses_by_gender = {gender: {response: 0 for response in response_options} for gender in genders}

    for i, row in df.iterrows():
        gender = get_gender(df, i)
        responses = get_single_multi_response(df, question, i)
        for response in responses:
            if (gender in responses_by_gender
                    and response in responses_by_gender[gender]):
                responses_by_gender[gender][response] += 1
                response_checker = True
        # add to overall count only if the respondent participated in this question
        if response_checker:
            gender_counts[gender] += 1
            response_checker = False

    # Create new dataframe and calculate percentage
    data = []
    for gender, responses in responses_by_gender.items():
        gender_count = gender_counts[gender]
        for response, count in responses.items():
            percentage = (count / gender_count)
            data.append({'Generation': gender,
                         'Response': response,
                         'Count': count,
                         'Percentage': percentage})

    return pd.DataFrame(data)


def get_region_data(df, question):
    response_options = get_multi_responses(df, question)
    response_checker = False
    region_counts = {region: 0 for region in get_region_list(df)}
    regions = get_region_list(df)
    responses_by_region = {region: {response: 0 for response in response_options} for region in regions}

    for i, row in df.iterrows():
        region = get_region(df, i)
        responses = get_single_multi_response(df, question, i)
        for response in responses:
            if (region in responses_by_region
                    and response in responses_by_region[region]):
                responses_by_region[region][response] += 1
                response_checker = True
        # add to overall count only if the respondent participated in this question
        if response_checker:
            region_counts[region] += 1
            response_checker = False

    # Create new dataframe and calculate percentage
    data = []
    for region, responses in responses_by_region.items():
        region_count = region_counts[region]
        for response, count in responses.items():
            percentage = (count / region_count)
            data.append({'Region': region,
                         'Response': response,
                         'Count': count,
                         'Percentage': percentage})

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
    import_data_name = '../csv_exports/cvg-2024-q4/raw-data.csv'
    data_frame = get_df_from_csv(import_data_name)
    my_question = 'What is causing you stress and anxiety at work? (Select all that apply)'
    export_data_name = 'Question 14.csv'

    export_data_to_csv(data_frame, my_question, export_data_name)
