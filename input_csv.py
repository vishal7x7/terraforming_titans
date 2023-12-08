import io
import json
import pdb
import re

import requests
import pandas as pd
from fastapi import UploadFile, File, FastAPI
from fastapi import Response
from pydantic import BaseModel

app = FastAPI()
host = "http://11.0.3.17:8503"


class Details(BaseModel) :
    title: str
    description: str
    jira_link: str
    tags: str


def __parse_response(data):
    answer = []
    for item in data :
        text = item["generated_text"]
        match1 = re.search("'resolution': '(.*?)'", text)
        match2 = re.search('"resolution": "(.*?)"', text)
        if match1 or match2 :
            resolution = match1.group(1) if match1 else match2.group(1)
            print(f"Resolution: {resolution}")
            answer.append(resolution)
        else :
            answer.append("Resolution not found")
    return answer


@app.post("/ask_question")
def get_answer(question: Details):
    print("inside ask_question: ", question)
    response = requests.post(f"{host}/chat", json=question.__dict__)
    print("response: ", response)
    data = __parse_response(response.json())
    return {"response": data}


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
            "tags": row.get("Category")
        }
        input_datas.append(data)

    print("input datas", input_datas)

    results = []
    for data in input_datas:
        print("data ---", data)
        response = requests.post(f"{host}/chat", json=data)
        print("reesponse ----", response.json())
        result = __parse_response(response.json())
        results.append(result[0])
    df["resolution"] = results

    updated_csv_path = "updated_file.csv"
    df.to_csv(updated_csv_path, index=False)
    # Prepare the CSV file for download
    csv_content = df.to_csv(index=False)
    response = Response(content=csv_content)
    response.headers["Content-Disposition"] = "attachment; filename=updated_file.csv"

    return response
