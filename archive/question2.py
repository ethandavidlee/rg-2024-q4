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


def get_single_response_options(df, question):
    if question in df.columns:
        unique_responses = df[question].unique()
        return unique_responses
    else:
        return None


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
    generation_counts = get_generation_counts(df)
    generations = get_generations_list()
    responses_by_generation = {generation: {response: 0 for response in response_options} for generation in generations}

    for i, row in df.iterrows():
        generation = get_generation(df, i)
        response = row[question]
        if generation in responses_by_generation and response in responses_by_generation[generation]:
            responses_by_generation[generation][response] += 1

    # Create new dataframe and calculate percentage
    data = []
    for generation, responses in responses_by_generation.items():
        region_count = generation_counts[generation]
        for response, count in responses.items():
            percentage = count / region_count
            data.append({'Generation': generation, 'Response': response, 'Count': count, 'Percentage': percentage})

    return pd.DataFrame(data)


def get_gender_data(df, question):
    response_options = get_single_response_options(df, question)
    gender_counts = get_gender_counts(df)
    genders = get_gender_list(df)
    responses_by_gender = {gender: {response: 0 for response in response_options} for gender in genders}

    for i, row in df.iterrows():
        gender = get_gender(df, i)
        response = row[question]
        if gender in responses_by_gender and response in responses_by_gender[gender]:
            responses_by_gender[gender][response] += 1

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
    region_counts = get_region_counts(df)
    regions = get_region_list(df)
    responses_by_region = {region: {response: 0 for response in response_options} for region in regions}

    for i, row in df.iterrows():
        region = get_region(df, i)
        response = row[question]
        if region in responses_by_region and response in responses_by_region[region]:
            responses_by_region[region][response] += 1

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
    import_data_name = 'raw-data.csv'
    data_frame = get_df_from_csv(import_data_name)
    my_question = ('How optimistic are you about the impact of the next presidential administration on your work and '
                    'career?')
    export_data_name = 'Question 2.csv'
    export_data_to_csv(data_frame, my_question, export_data_name)