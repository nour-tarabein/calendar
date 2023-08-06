from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import sqlite3


app = Flask(__name__)



def create_table():
    with sqlite3.connect('calendar.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('create table if not exists events (id integer primary key autoincrement, date date, event text)')
        conn.commit()

def add_event(date, event):
    with sqlite3.connect('calendar.sqlite') as conn:
        cursor = conn.cursor()
        iso_date = datetime.strptime(date, "%Y-%m-%d")
        sqlite_date = datetime.strftime(iso_date, "%Y-%m-%d %H:%M:%S")
        cursor.execute('insert into events (date, event) values(?, ?)', (sqlite_date, event))
        event_id = cursor.lastrowid
        conn.commit()
        return event_id

def get_events():
    with sqlite3.connect('calendar.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('select * from events')
        return cursor.fetchall()

def delete_event(event_id):
    with sqlite3.connect('calendar.sqlite') as conn:
        cursor = conn.cursor()
        print(event_id)
        cursor.execute('delete from events where id = ?', (event_id,))
        conn.commit()

def update_event(event_id, date, event):
    with sqlite3.connect('calendar.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('update events set date = ?, event = ? where id = ?', (date, event, event_id))
        conn.commit()

@app.route('/')
def home():
    events = get_events()
    return render_template("index.html",events=events)


@app.route('/add', methods=['POST'])
def add_event_route():
       if request.method == 'POST':
           date = datetime.strptime(request.json.get('date'), '%Y-%m-%d').date().isoformat()
           event = request.json.get('event')
           event_id = add_event(date, event)
           return jsonify({"status": "success", "event_id": event_id})
       return jsonify({"status": "error"})


@app.route('/get-events', methods=['GET'])
def get_event_route():
       events_data = get_events()
       events = []
       for e in events_data:
           event = {"id": e[0], "title": e[2], "start": e[1], "allDay": True}
           events.append(event)
       return jsonify(events)


@app.route('/delete/<int:event_id>', methods=['DELETE'])
def delete_event_route(event_id):
    delete_event(event_id)
    return jsonify({"status": "success"}), 200
    
@app.route('/update/<int:event_id>', methods=['PATCH'])
def update_event_route(event_id):
       if request.method == 'PATCH':
           data = request.get_json()
           date = datetime.strptime(data.get('date'), '%Y-%m-%d').date().isoformat()
           event = data.get('event')
           update_event(event_id, date, event)
           return jsonify({"status": "success"})
       return jsonify({"status": "error"})

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PATCH,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response



if __name__ =="__main__":
        create_table()
        app.run()

