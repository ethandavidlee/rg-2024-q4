import pandas as pd
import datetime


def get_df_from_gsheet(key, sheet):
    url = f'https://docs.google.com/spreadsheet/ccc?key={key}&output=xlsx'
    df = pd.read_excel(url, sheet_name=sheet)
    return df


def write_gsheet_to_csv(df, filename=None):
    """
    Write the given dictionary to a CSV file.
    """
    if filename is None:
        filename = f"{datetime.date.today()}.csv"

    # Using pandas to_csv method to write DataFrame to CSV
    df.to_csv(filename, index=False)

    print(f"Data successfully written to {filename}")


if __name__ == "__main__":
    # https://docs.google.com/spreadsheets/d/1KDxCu1ML9fh2em6_Fqm5WumsiAyaJYowpRavf2eLBBA/edit?gid=0#gid=0

    gsheetkey = "1KDxCu1ML9fh2em6_Fqm5WumsiAyaJYowpRavf2eLBBA"
    sheet_name = 'Raw Data'
    filename = 'raw-data.csv'

    raw_data = get_df_from_gsheet(gsheetkey, sheet_name)
    write_gsheet_to_csv(raw_data, filename)
