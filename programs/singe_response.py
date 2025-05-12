import pandas as pd
import datetime
import sys
from cross_question_functions import *


def get_single_response_options(df, question):
    if question in df.columns:
        unique_responses = df[question].dropna().unique()
        return unique_responses
    else:
        print('Question not available. Please check that the provided question is valid for this sheet.')
        sys.exit(1)


def get_overall_data(df, question):
    response_options = get_single_response_options(df, question)
    overall_count = 0
    responses = {response: 0 for response in response_options}

    for _, row in df.iterrows():
        response = row[question]
        if response in responses:
            responses[response] += 1
            overall_count += 1

    # Create new dataframe and calculate percentage
    data = []
    for response, count in responses.items():
        percentage = count / overall_count
        data.append({'All Respondents': 'All Respondents', 'Response': response, 'Count': count, 'Percentage': percentage})

    return pd.DataFrame(data)


def get_generation_data(df, question):
    response_options = get_single_response_options(df, question)
    generation_counts = {generation: 0 for generation in get_generations_list()}
    generations = get_generations_list()
    responses_by_generation = {generation: {response: 0 for response in response_options} for generation in generations}

    for i, row in df.iterrows():
        generation = get_generation(df, i)
        response = row[question]
        if generation in responses_by_generation and response in responses_by_generation[generation]:
            responses_by_generation[generation][response] += 1
            generation_counts[generation] += 1

    # Create new dataframe and calculate percentage
    data = []
    for generation, responses in responses_by_generation.items():
        generation_count = generation_counts[generation]
        for response, count in responses.items():
            percentage = count / generation_count
            data.append({'Generation': generation, 'Response': response, 'Count': count, 'Percentage': percentage})

    return pd.DataFrame(data)


def get_age_data(df, question):
    response_options = get_single_response_options(df, question)
    ages = get_age_list(df)
    age_counts = {age: 0 for age in ages}
    responses_by_age = {age: {response: 0 for response in response_options} for age in ages}

    for i, row in df.iterrows():
        age = get_age(df, i)
        response = row[question]
        if age in responses_by_age and response in responses_by_age[age]:
            responses_by_age[age][response] += 1
            age_counts[age] += 1

    # Create new dataframe and calculate percentage
    data = []
    for age, responses in responses_by_age.items():
        age_count = age_counts[age]
        for response, count in responses.items():
            percentage = count / age_count
            data.append({'Age': age, 'Response': response, 'Count': count, 'Percentage': percentage})

    return pd.DataFrame(data)


def get_gender_data(df, question):
    response_options = get_single_response_options(df, question)
    genders = get_gender_list(df)
    gender_counts = {gender: 0 for gender in genders}
    responses_by_gender = {gender: {response: 0 for response in response_options} for gender in genders}

    for i, row in df.iterrows():
        gender = get_gender(df, i)
        response = row[question]
        if gender in responses_by_gender and response in responses_by_gender[gender]:
            responses_by_gender[gender][response] += 1
            gender_counts[gender] += 1

    # Create new dataframe and calculate percentage
    data = []
    for gender, responses in responses_by_gender.items():
        gender_count = gender_counts[gender]
        for response, count in responses.items():
            percentage = count/gender_count
            data.append({'Gender': gender, 'Response': response, 'Count': count, 'Percentage': percentage})

    return pd.DataFrame(data)


def get_region_data(df, question):
    response_options = get_single_response_options(df, question)
    region_counts = {region: 0 for region in get_region_list(df)}
    regions = get_region_list(df)
    responses_by_region = {region: {response: 0 for response in response_options} for region in regions}

    for i, row in df.iterrows():
        region = get_region(df, i)
        response = row[question]
        if region in responses_by_region and response in responses_by_region[region]:
            responses_by_region[region][response] += 1
            region_counts[region] += 1

    # Create new dataframe and calculate percentage
    data = []
    for region, responses in responses_by_region.items():
        region_count = region_counts[region]
        for response, count in responses.items():
            percentage = count/region_count
            data.append({'Region': region, 'Response': response, 'Count': count, 'Percentage': percentage})

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
    write_section_to_csv(get_overall_data(df, question), 'Overall Data', filename, 'w')
    write_section_to_csv(get_gender_data(df, question), 'Gender Data', filename, 'a')
#    write_section_to_csv(get_generation_data(df, question), 'Generation Data', filename, 'a')
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
