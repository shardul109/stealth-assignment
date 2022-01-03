from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import requests
import json

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
        return res.json()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')


if __name__ == '__main__':
    run("main:app", host="127.0.0.1", port=5002, reload=True)
