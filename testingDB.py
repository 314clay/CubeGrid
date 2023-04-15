import csv

from flask import Flask, request, render_template, send_file, make_response
from datetime import datetime
import os

app = Flask(__name__)

with open('output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    titles = []
    for row in reader:
        if not row['Alg']: continue
        title = ' '.join([row['Goal'], row['Set'], row['Subset'], ':', row['Alg']])
        titles.append(title)

DATA_FILE = 'data.txt'
titles = [title for title in titles if title]
SUBSESSIONS_FILE_TEMPLATE = '{}.txt'
SPECIAL_SUBSESSIONS_FILE_TEMPLATE = 'special_{}.txt' # only allow alphanumeric

def load_special_subsession_ids(session_id):
    special_subsessions_file = SPECIAL_SUBSESSIONS_FILE_TEMPLATE.format(session_id)
    if not os.path.exists(special_subsessions_file):
        return []
    with open(special_subsessions_file, 'r') as f:
        return f.read().split(',')

def save_special_subsession_ids(session_id, special_subsession_ids):
    with open(SPECIAL_SUBSESSIONS_FILE_TEMPLATE.format(session_id), 'w') as f:
        f.write(','.join(special_subsession_ids))

def load_data():
    with open(DATA_FILE, 'r') as f:
        res = f.read().splitlines()
        return res

def save_data(data_list):
    with open(DATA_FILE, 'w') as f:
        f.write('\n'.join(data_list))

def load_subsession_ids(session_id):
    subsession_ids_file = SUBSESSIONS_FILE_TEMPLATE.format(session_id)
    if not os.path.exists(subsession_ids_file):
        return titles
    with open(subsession_ids_file, 'r') as f:
        return f.read().split(',')

def save_subsession_ids(session_id, subsession_ids):
    with open(SUBSESSIONS_FILE_TEMPLATE.format(session_id), 'w') as f:
        f.write(','.join(subsession_ids))

def filter_data(data_list, session_id, subsession_id):
    return [line for line in data_list[::-1] if line.startswith(f'{session_id},{subsession_id},')]

@app.route('/', methods=['GET', 'POST'], defaults={'url_session_id': None})
@app.route('/<string:url_session_id>', methods=['GET', 'POST'])
def home(url_session_id):
    session_id = url_session_id or request.form.get('session_id', 'def')
    subsession_id = request.form.get('subsession_id')
    data = request.form.get('data')
    count = request.form.get('count')
    updated_subsession_ids = request.form.get('subsession_ids')


    special_subsession_ids = []
    if session_id is not None:
        special_subsession_ids = load_special_subsession_ids(session_id)

    if request.form.get('toggle_special'):
        toggle_subsession_id = request.form.get('toggle_subsession_id')
        if toggle_subsession_id in special_subsession_ids:
            special_subsession_ids.remove(toggle_subsession_id)
        else:
            special_subsession_ids.append(toggle_subsession_id)
        if session_id is not None:
            save_special_subsession_ids(session_id, special_subsession_ids)

    subsession_ids = []
    if session_id is not None:
        subsession_ids = load_subsession_ids(session_id)

    if session_id is not None and updated_subsession_ids:
        subsession_ids = [subsession_id.strip() for subsession_id in updated_subsession_ids.split(',')]
        save_subsession_ids(session_id, subsession_ids)

    data_list = load_data()
    if session_id is not None and subsession_id and data and count:
        timestamp = datetime.now().strftime("%-m-%d %-I:%M %p")
        data_list.append(f'{session_id},{subsession_id},{data},{count},{timestamp}')
        save_data(data_list)

    if session_id is not None and subsession_id:
        data_list = filter_data(data_list, session_id, subsession_id)

    data_list = [tuple(line.split(',')) for line in data_list]

    return render_template('home.html', session_id=session_id, subsession_ids=subsession_ids, selected_subsession=subsession_id, data_list=data_list, special_subsession_ids=special_subsession_ids, cache_version = 1)

if __name__ == '__main__':
    app.run(debug=True)