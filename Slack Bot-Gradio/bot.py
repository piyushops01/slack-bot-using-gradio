import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from gradio_client import Client


# Load environment variables
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

print("Bot token loaded:", bool(SLACK_BOT_TOKEN))
print("App token loaded:", bool(SLACK_APP_TOKEN))


# Create Slack app
app = App(token=SLACK_BOT_TOKEN)


# Connect to your local Gradio app
gradio_client = Client("http://127.0.0.1:7860")


@app.event("app_mention")
def handle_app_mention_events(body, say):

    # Get the message
    message = body["event"]["text"]

    # Get bot's user ID
    bot_user_id = body["authorizations"][0]["user_id"]

    # Remove the bot mention
    clean_message = message.replace(
        f"<@{bot_user_id}>", ""
    ).strip()

    print("Message received from Slack:", clean_message)

    # Send message to Gradio
    result = gradio_client.predict(
        clean_message,
        api_name="/predict"
    )

    print("Response from Gradio:", result)

    # Send Gradio response back to Slack
    say(str(result))


if __name__ == "__main__":

    print("Starting Slack bot...")

    handler = SocketModeHandler(
        app,
        SLACK_APP_TOKEN
    )

    handler.start()