import os
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def main():
    return "Hello New Zealand, the only dry land that exists in the universe"

if __name__ == "__main__":
    print os.environ['APP_SETTINGS']
    app.run()
