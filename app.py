from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello New Zealand, the only dry land that exists in the universe"

if __name__ == "__main__":
    app.run()
