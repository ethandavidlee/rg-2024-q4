import pandas as pd
import datetime


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


# def get_generation_counts(df):
#     if 'Year Of Birth' not in df.columns and 'Age' not in df.columns:
#         return None
#
#     generations = get_generations_list()
#     generation_counts = {generation: 0 for generation in generations}
#     current_year = datetime.datetime.now().year
#
#     if 'Year Of Birth' in df.columns:
#         year_counts = df['Year Of Birth'].dropna().value_counts()
#         generation_counts = {'Gen Z': 0, 'Millennial': 0, 'Gen X': 0, 'Baby Boomer': 0}
#         for year, count in year_counts.items():
#             if 1997 <= year <= 2012:
#                 generation_counts['Gen Z'] += count
#             elif 1981 <= year <= 1996:
#                 generation_counts['Millennial'] += count
#             elif 1965 <= year <= 1980:
#                 generation_counts['Gen X'] += count
#             elif 1946 <= year <= 1964:
#                 generation_counts['Baby Boomer'] += count
#
#     elif 'Age' in df.columns:
#         age_counts = df['Age'].dropna().value_counts()
#         for age, count in age_counts.items():
#             birth_year = current_year - age
#             if 1997 <= birth_year <= 2012:
#                 generation_counts['Gen Z'] += count
#             elif 1981 <= birth_year <= 1996:
#                 generation_counts['Millennial'] += count
#             elif 1965 <= birth_year <= 1980:
#                 generation_counts['Gen X'] += count
#             elif 1946 <= birth_year <= 1964:
#                 generation_counts['Baby Boomer'] += count
#
#     else:
#         return None
#
#     return pd.Series(generation_counts)
#
#
# def get_gender_counts(df):
#     if 'Gender' in df.columns:
#         gender_counts = df['Gender'].dropna().value_counts()
#         return gender_counts
#     else:
#         return pd.Series(dtype=int)
#
#
# def get_region_counts(df):
#     if 'US Region' in df.columns:
#         region_counts = df['US Region'].dropna().value_counts()
#         return region_counts
#     elif 'UK Region' in df.columns:
#         subregion_counts = df['UK Region'].dropna().value_counts()
#         not_counted = 0
#         region_counts = {'London': 0, 'Northern England': 0, 'Midlands (England)': 0, 'Southern England': 0,
#                          'Scotland': 0, 'Wales': 0, 'Northern Ireland': 0}
#         for subregion, count in subregion_counts.items():
#             if subregion == 'London':
#                 region_counts['London'] += count
#             elif (subregion == 'North East (England' or subregion == 'North West (England)'  # Pollfish mistake with )
#                   or subregion == 'Yorkshire And The Humber'):
#                 region_counts['Northern England'] += count
#             elif subregion == 'West Midlands (England)' or subregion == 'East Midlands (England)':
#                 region_counts['Midlands (England)'] += count
#             elif (subregion == 'South East (England)' or subregion == 'East Of England'
#                   or subregion == 'South West (England)'):
#                 region_counts['Southern England'] += count
#             elif subregion == 'Scotland':
#                 region_counts['Scotland'] += count
#             elif subregion == 'Wales':
#                 region_counts['Wales'] += count
#             elif subregion == 'Northern Ireland':
#                 region_counts['Northern Ireland'] += count
#             else:
#                 not_counted += count
#         print(f'Not included in region counts: {not_counted}')
#         return region_counts
#     else:
#         return pd.Series(dtype=int)
#

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
        return None

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
    my_question = 'How often have you felt the following at work?'
    export_data_name = 'Question 13.csv'

    export_data_to_csv(data_frame, my_question, export_data_name)

