import pandas as pd
import csv
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def preprocess_data(data):
    # Replace 'inf', '-inf' with a large finite number or another placeholder, and 'nan' with an empty string
    return data.replace([np.inf, -np.inf], np.nan).fillna('')


def write_csv_to_gsheet(filename, gsheetkey, sheet_name):
    key_file_path = '/my_credentials.json'
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']

    # Authorizing with the Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, scope)
    client = gspread.authorize(creds)

    # Accessing the spreadsheet
    sheet = client.open_by_key(gsheetkey)
    try:
        worksheet = sheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")

    # Reading the CSV file
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

    # Updating the worksheet with CSV data
    # If the range is not specified, update assumes the range starting at 'A1'
    worksheet.update('A1', values, value_input_option='USER_ENTERED')

    print(f"Data successfully written to {sheet_name} in Google Sheet with key {gsheetkey}")


if __name__ == "__main__":
    filename = '../csv_exports/Question 4.csv'
    gsheetkey = "1KDxCu1ML9fh2em6_Fqm5WumsiAyaJYowpRavf2eLBBA"
    sheet_name = 'Question 4'
    write_csv_to_gsheet(filename, gsheetkey, sheet_name)

