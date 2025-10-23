from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import pandas as pd
import os
import tempfile

def excel_to_text(excel_file_path: str) -> str:
    xls = pd.ExcelFile(excel_file_path)
    text_data = ""
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        text_data += f"\n\n--- {sheet_name} ---\n"
        text_data += df.to_string(index=False)
    return text_data

def get_temp_file_path(filename: str) -> str:
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)