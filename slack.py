from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
#####
from pydantic import BaseModel

app = FastAPI()

slack_bot_token = "xoxb-2196501177986-6338286699504-KLFa2W2LEPFIDGubvRkFTigW"
client = WebClient(token=slack_bot_token)


class SlackEvent(BaseModel):
    type: str
    user: str
    text: str
    channel: str


@app.post("/slack/events")
async def slack_events(event: SlackEvent):
    if event.type == "url_verification":
        return JSONResponse(content={"challenge": event["challenge"]}, status_code=200)

    if event.type == "message":
        handle_message(event)

    return {"status": "OK"}


def handle_message(event):
    channel_id = event.channel
    user_id = event.user
    text = event.text

    # Call your API here and get the response
    print("Slack Integration", event)
    api_response = call_your_api(text)

    # Send the API response back to the Slack channel
    message = f"<@{user_id}> {api_response}"

    try:
        client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
        print(f"Error posting message to Slack: {e.response['error']}")


def call_your_api(text):
    # Replace the following with the actual endpoint and parameters for your API
    api_endpoint = "http://11.0.3.17:8503/chat"

    try:
        data = {}
        # Make a request to your API
        print("Slack", text)
        response = requests.post(api_endpoint, data=text)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and extract the relevant information from the API response
            api_data = response.json()
            result = api_data.get("result", "No result found")

            # Return the result to be sent to Slack
            return f"API Response: {result}"

        # Handle other status codes if needed
        else:
            return f"Failed to get data from API. Status Code: {response.status_code}"

    except requests.RequestException as e:
        # Handle any exceptions that may occur during the API request
        return f"Error connecting to API: {str(e)}"