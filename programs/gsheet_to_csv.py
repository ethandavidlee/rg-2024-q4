import pandas as pd
import datetime


def get_df_from_gsheet(key, sheet):
    """
    Takes a Google Sheet key and a sheet name and returns the data in that sheet as a Pandas dataframe.
    """
    url = f'https://docs.google.com/spreadsheet/ccc?key={key}&output=xlsx'
    df = pd.read_excel(url, sheet_name=sheet)
    return df


def write_gsheet_to_csv(df, filename=None):
    """
    Write the dataframe to a CSV file.
    """
    if filename is None:
        filename = f"{datetime.date.today()}.csv"

    # Using pandas to_csv method to write DataFrame to CSV
    df.to_csv(filename, index=False)

    print(f"Data successfully written to {filename}")


if __name__ == "__main__":
    # https://docs.google.com/spreadsheets/d/1p3z3WnzGesafG7se-6eJn5vfGaiErQiq_VHOz0Iu8hU/

    gsheetkey = '1p3z3WnzGesafG7se-6eJn5vfGaiErQiq_VHOz0Iu8hU'
    sheet_name = 'Raw Data'
    filename = '../csv_exports/rg-2025-q2/raw-data.csv'

    raw_data = get_df_from_gsheet(gsheetkey, sheet_name)
    write_gsheet_to_csv(raw_data, filename)
