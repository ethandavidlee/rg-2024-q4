import csv
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def preprocess_data(data):
    # Replace 'inf', '-inf' with a large finite number or another placeholder, and 'nan' with an empty string
    return data.replace([np.inf, -np.inf], np.nan).fillna('')


def write_csv_to_gsheet(filename, gsheetkey, sheet_name):
    """
    Takes a local CSV file and exports it to the designated Google Sheet under a new tab defined by sheet_name.
    """
    key_file_path = '../my_credentials.json'
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']

    # Authorize with Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, scope)
    client = gspread.authorize(creds)

    # Access Google Sheet
    sheet = client.open_by_key(gsheetkey)
    try:
        worksheet = sheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")

    # Read CSV file
    with open(filename, "r") as f:
        reader = csv.reader(f)
        max_length = 0
        values = []
        for row in reader:
            values.append(row)
            if len(row) > max_length:
                max_length = len(row)

        # Pad rows with fewer columns than the maximum
        for row in values:
            row.extend([""] * (max_length - len(row)))

    # Updating the Google Sheet CSV data starting at 'A1'
    worksheet.update('A1', values, value_input_option='USER_ENTERED')

    print(f"Data successfully written to {sheet_name} in Google Sheet with key {gsheetkey}")


if __name__ == "__main__":
    # Set constants for this survey
    gsheetkey = '1p3z3WnzGesafG7se-6eJn5vfGaiErQiq_VHOz0Iu8hU'
    report_folder = 'rg-2025-q2'

    # Export all survey data to Google Sheet
    for num in range(3,17):
        filename = f'Question {num}'
        filepath = f'../csv_exports/{report_folder}/{filename}.csv'
        sheet_name = filename
        write_csv_to_gsheet(filepath, gsheetkey, sheet_name)

    # Write demographics to GSheet
#    demographics_filepath = f'../csv_exports/{report_folder}/demographics.csv'
#    write_csv_to_gsheet(demographics_filepath, gsheetkey, 'Demographics')
