from flask import Flask
from data_manager import html_map

app = Flask(__name__)


@app.route('/')
def index():
    return html_map


if __name__ == '__main__':
    app.run()
