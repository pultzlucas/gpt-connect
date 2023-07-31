from flask import Flask
from flask_cors import CORS
from libs.csv_controller import CsvController
from flask import request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from libs.splitcsv import split_csv_file
import logging

app = Flask(__name__)
CORS(app)

csv = CsvController()

MAX_ROWS_BY_CSV = 1000

class InputFolderListener(FileSystemEventHandler):
    def on_created(self, event):
        try:
            with open(event.src_path, 'r', encoding="utf8") as f:
                lines = f.read().split('\n')
                print(f.name, 'was added')
            if len(lines) > MAX_ROWS_BY_CSV:
                split_csv_file(f.name, MAX_ROWS_BY_CSV)
                os.remove(f.name)
                return
        except FileNotFoundError:
            return
    def on_deleted(self, event):
        if os.path.basename(event.src_path) in csv.input_files:
            csv.input_files.remove(os.path.basename(event.src_path))
            print(os.path.basename(event.src_path), 'was removed')

observer = Observer()
observer.schedule(InputFolderListener(), path='./data/input', recursive=False)
observer.start()

@app.get("/")
def root():
    return "GPT Scraping Hub"

@app.get("/csv")
def get_csv():
    return csv.get_csv()

@app.post("/csv")
def post_csv():
    return csv.receive_csv(request.data, request.args.get(key='filename', type=str))

if __name__ == '__main__':
    app.run(debug=False, port=5123)