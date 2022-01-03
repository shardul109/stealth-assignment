import json
import gspread
import pandas as pd
import requests
from df2gspread import df2gspread as d2g
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from oauth2client.service_account import ServiceAccountCredentials
from uvicorn import run

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get('/load_into_sheets', tags=['functionality'])
def shopify_to_sheets():
    try:
        with open('secrets.json') as f:
            data = json.load(f)
        res = requests.get(
            f'https://{data["apikey"]}:{data["password"]}@{data["storename"]}.myshopify.com/admin/api/2021-10/products.json')
        d = res.json()['products']
        df = pd.DataFrame(data=d)
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'jsonFileFromGoogle.json', scope)
        client = gspread.authorize(credentials)
        spreadsheet_key = '1vwhM_7wRADbA9nO4BrQjetETUj9D1AmhQjr2f48uj88'
        wks_name = 'stealth-shopify-api'
        d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
        return {
            'detail': 'success'
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')


if __name__ == '__main__':
    run("main:app", host="0.0.0.0", port=5002, reload=True)
