import requests


def download_gsheet_csv(file_id, sheet_id):
    r = requests.get(f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&id={file_id}&gid={sheet_id}")
    return r.content.decode("utf-8")
