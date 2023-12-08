import io
import requests
import pandas as pd
from fastapi import UploadFile, File, FastAPI

app = FastAPI()
host = "http://11.0.3.17:8503"


@app.post("/uploadfile/")
async def process_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    input_datas = []
    for index, row in df.iterrows():
        data = {
            "title": row.get("Summary"),
            "description": row.get("Description")[:100],
            "jira_link": row.get("Issue key"),
        }
        input_datas.append(data)

    print("input datas", input_datas)

    results = []
    for data in input_datas:
        print("data ---", data)
        response = requests.post(f"{host}/chat", json=data)
        results.append(response.json())

    return {"results": results}
