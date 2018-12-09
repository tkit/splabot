import os

if "API_TOKEN" not in os.environ:
    print("error: API_TOKEN is absent")
    exit(1)
API_TOKEN = os.getenv("API_TOKEN")
DEFAULT_REPLY = "sorry I can't understand"
PLUGINS = ['plugins']
