import pandas as pd
import datetime
import sys
from cross_question_functions import *


def get_matrix_statements(df, question):
    if question not in df.columns:
        return None

    statements = set()

    # Iterate through first row in the specified column
    for entry in df[question].dropna().unique():
        # Split the entry into individual key-value pairs
        items = entry.split(" | ")
        for item in items:
            if ':' in item:
                key, value = item.split(":", 1)
                statements.add(key.strip())

    return list(statements)


def get_matrix_responses(df, question):
    if question not in df.columns:
        print('Question not available. Please check that the provided question is valid for this sheet.')
        sys.exit(1)

    responses = set()

    # Iterate through each row in the specified column
    for entry in df[question].dropna().unique():
        # Split the entry into individual key-value pairs
        items = entry.split(" | ")
        for item in items:
            if ':' in item:
                key, value = item.split(":", 1)
                responses.add(value.strip())

    return list(responses)


def get_single_matrix_response(df, question, respondent, statement):
    if question in df.columns:
        try:
            items = df.loc[respondent, question].split(" | ")
        # Respondent didn't respond to this question
        except AttributeError:
            return None
        for item in items:
            if ':' in item:
                key, value = item.split(":", 1)
                stripped_key = key.strip(' ')
                stripped_value = value.strip(' ')
                if stripped_key == statement:
                    return stripped_value
    else:
        return None


def get_overall_data_as_matrix(df, question):
    statements = get_matrix_statements(df, question)
    response_options = get_matrix_responses(df, question)
    response_checker = False
    overall_count = 0
    response_data = {statement: {response: 0 for response in response_options} for statement in statements}

    for i, row in df.iterrows():
        for statement in statements:
            response = get_single_matrix_response(df, question, i, statement)
            if response in response_options:
                response_checker = True
                response_data[statement][response] += 1

        # Add to count only if respondent answered this question
        if response_checker:
            overall_count += 1
            response_checker = False

    # Calculate percentages
    percentage_data = {}
    for statement, responses in response_data.items():
        percentage_data[statement] = {response: (count / overall_count) for response, count in responses.items()}

    # Convert to DataFrame and insert the statements as the first column
    data = pd.DataFrame(percentage_data).T
    data.insert(0, 'All respondents', data.index)

    return pd.DataFrame(data)


def get_generation_data(df, question):
    statements = get_matrix_statements(df, question)
    response_options = get_matrix_responses(df, question)
    response_checker = False
    generation_counts = {generation: 0 for generation in get_generations_list()}
    generations = get_generations_list()
    responses_by_generation = {generation:
                                       {statement:
                                            {response: 0 for response in response_options}
                                        for statement in statements}
                                   for generation in generations}

    for i, row in df.iterrows():
        generation = get_generation(df, i)
        for statement in statements:
            response = get_single_matrix_response(df, question, i, statement)
            if (generation in responses_by_generation
                    and statement in responses_by_generation[generation]
                    and response in responses_by_generation[generation][statement]
            ):
                responses_by_generation[generation][statement][response] += 1
                response_checker = True
        if response_checker == True:
            generation_counts[generation] += 1
            response_checker = False

    # Initialize a list to hold data for all generations
    all_data_frames = []

    # Calculate percentages and prepare the DataFrame for each generation
    for generation, statements in responses_by_generation.items():
        percentage_data = {}
        generation_count = generation_counts[generation]
        for statement, responses in statements.items():
            percentage_data[statement] = {}
            for response, count in responses.items():
                percentage_data[statement][response] = (count / generation_count)

        # Create a DataFrame for the current generation
        gen_df = pd.DataFrame(percentage_data).T
        gen_df['Generation'] = generation  # Add the generation for each column
        all_data_frames.append(gen_df)

    # Concatenate all generation data frames into a single DataFrame
    final_data = pd.concat(all_data_frames, axis=0)
    final_data.reset_index(inplace=True, drop=False)
    final_data.rename(columns={'index': 'Statement'}, inplace=True)

    return final_data


def get_age_data(df, question):
    statements = get_matrix_statements(df, question)
    response_options = get_matrix_responses(df, question)
    response_checker = False
    ages = get_age_list(df)
    age_counts = {age: 0 for age in ages}
    responses_by_age = {age:
                            {statement:
                                 {response: 0 for response in response_options}
                             for statement in statements}
                        for age in ages}

    for i, row in df.iterrows():
        age = get_age(df, i)
        for statement in statements:
            response = get_single_matrix_response(df, question, i, statement)
            if (age in responses_by_age
                    and statement in responses_by_age[age]
                    and response in responses_by_age[age][statement]
            ):
                responses_by_age[age][statement][response] += 1
                response_checker = True
        if response_checker:
            age_counts[age] += 1
            response_checker = False

    # Initialize a list to hold data for all ages
    all_data_frames = []

    # Calculate percentages and prepare the DataFrame for each age
    for age, statements in responses_by_age.items():
        percentage_data = {}
        age_count = age_counts[age]
        for statement, responses in statements.items():
            percentage_data[statement] = {}
            for response, count in responses.items():
                percentage_data[statement][response] = (count / age_count)

        # Create a DataFrame for the current age
        age_df = pd.DataFrame(percentage_data).T
        age_df['Age'] = age  # Add the age for each column
        all_data_frames.append(age_df)

    # Concatenate all age data frames into a single DataFrame
    final_data = pd.concat(all_data_frames, axis=0)
    final_data.reset_index(inplace=True, drop=False)
    final_data.rename(columns={'index': 'Statement'}, inplace=True)

    return final_data


def get_gender_data(df, question):
    statements = get_matrix_statements(df, question)
    response_options = get_matrix_responses(df, question)
    gender_counts = {gender: 0 for gender in get_gender_list(df)}
    response_checker = False
    genders = get_gender_list(df)
    responses_by_gender = {gender:
                               {statement:
                                    {response: 0 for response in response_options}
                                for statement in statements}
                           for gender in genders}

    for i, row in df.iterrows():
        gender = get_gender(df, i)
        for statement in statements:
            response = get_single_matrix_response(df, question, i, statement)
            if (gender in responses_by_gender
                    and statement in responses_by_gender[gender]
                    and response in responses_by_gender[gender][statement]
            ):
                responses_by_gender[gender][statement][response] += 1
                response_checker = True
        if response_checker == True:
            gender_counts[gender] += 1
            response_checker = False

    # Initialize a list to hold data for all generations
    all_data_frames = []

    # Calculate percentages and prepare the DataFrame for each generation
    for gender, statements in responses_by_gender.items():
        percentage_data = {}
        generation_count = gender_counts[gender]
        for statement, responses in statements.items():
            percentage_data[statement] = {}
            for response, count in responses.items():
                percentage_data[statement][response] = (count / generation_count)

        # Create a DataFrame for the current gender
        gender_df = pd.DataFrame(percentage_data).T
        gender_df['Gender'] = gender  # Add the gender for each column
        all_data_frames.append(gender_df)

    # Concatenate all generation data frames into a single DataFrame
    final_data = pd.concat(all_data_frames, axis=0)
    final_data.reset_index(inplace=True, drop=False)
    final_data.rename(columns={'index': 'Statement'}, inplace=True)

    return final_data


def get_region_data(df, question):
    statements = get_matrix_statements(df, question)
    response_options = get_matrix_responses(df, question)
    region_counts = {region: 0 for region in get_region_list(df)}
    response_checker = False
    regions = get_region_list(df)
    responses_by_region = {region:
                                       {statement:
                                            {response: 0 for response in response_options}
                                        for statement in statements}
                                   for region in regions}

    for i, row in df.iterrows():
        region = get_region(df, i)
        for statement in statements:
            response = get_single_matrix_response(df, question, i, statement)
            if (region in responses_by_region
                    and statement in responses_by_region[region]
                    and response in responses_by_region[region][statement]
            ):
                responses_by_region[region][statement][response] += 1
                response_checker = True
        if response_checker == True:
            region_counts[region] += 1
            response_checker = False

    # Initialize a list to hold data for all generations
    all_data_frames = []

    # Calculate percentages and prepare the DataFrame for each region
    for region, statements in responses_by_region.items():
        percentage_data = {}
        region_count = region_counts[region]
        for statement, responses in statements.items():
            percentage_data[statement] = {}
            for response, count in responses.items():
                percentage_data[statement][response] = (count / region_count)

        # Create a DataFrame for the current region
        region_df = pd.DataFrame(percentage_data).T
        region_df['Region'] = region  # Add the region for each column
        all_data_frames.append(region_df)

    # Concatenate all generation data frames into a single DataFrame
    final_data = pd.concat(all_data_frames, axis=0)
    final_data.reset_index(inplace=True, drop=False)
    final_data.rename(columns={'index': 'Statement'}, inplace=True)

    return final_data


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
    overall_data = get_overall_data_as_matrix(df, question)
    gender_data = get_gender_data(df, question)
    # generation_data = get_generation_data(df, question)
    region_data = get_region_data(df, question)

    # Write overall data or print warning
    write_section_to_csv(overall_data, 'Overall Data', filename, 'w')

    # Append other data sections to the CSV with separation
    write_section_to_csv(gender_data, 'Gender Data', filename, 'a')
    # write_section_to_csv(generation_data, 'Generation Data', filename, 'a')
    write_section_to_csv(get_age_data(df, question), 'Age Data', filename, 'a')
    write_section_to_csv(region_data, 'Region Data', filename, 'a')


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

