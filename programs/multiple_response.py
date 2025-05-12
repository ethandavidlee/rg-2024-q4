import pandas as pd
import datetime
import sys
from cross_question_functions import *


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


def get_age_data(df, question):
    response_options = get_multi_responses(df, question)
    ages = get_age_list(df)
    age_counts = {age: 0 for age in ages}
    response_checker = False
    responses_by_age = {age: {response: 0 for response in response_options} for age in ages}

    for i, row in df.iterrows():
        age = get_age(df, i)
        responses = get_single_multi_response(df, question, i)
        for response in responses:
            if (age in responses_by_age
                    and response in responses_by_age[age]):
                responses_by_age[age][response] += 1
                response_checker = True
        # add to overall count only if the respondent participated in this question
        if response_checker:
            age_counts[age] += 1
            response_checker = False

    # Create new dataframe and calculate percentage
    data = []
    for age, responses in responses_by_age.items():
        for response, count in responses.items():
            percentage = (count / age_counts[age])
            data.append({'Age': age,
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
    # Write overall data or print warning
    write_section_to_csv(get_overall_data(df, question), 'Overall Data', filename, 'w')
    write_section_to_csv(get_gender_data(df, question), 'Gender Data', filename, 'a')
  #  write_section_to_csv(get_generation_data(df, question), 'Generation Data', filename, 'a')
    write_section_to_csv(get_age_data(df, question), 'Age Data', filename, 'a')
    write_section_to_csv(get_region_data(df, question), 'Region Data', filename, 'a')


if __name__ == "__main__":
    # Set variables for analysis
    report_folder = 'rg-2025-q2'
    question_number = '16'
    question_text = 'When you define your own career success, how important are the following factors?'

    # Export data to CSV
    import_data_name = f'../csv_exports/{report_folder}/raw-data.csv'
    data_frame = get_df_from_csv(import_data_name)
    my_question = f'Q{question_number}: {question_text}'
    export_data_name = f'Question {question_number}.csv'
    export_data_to_csv(data_frame, my_question, export_data_name)
