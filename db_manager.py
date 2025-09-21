import os
import sqlite3
import json

DB_PATH = 'db/profiles.db'

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, profile TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, desc TEXT, due TEXT, status TEXT)''')
    conn.commit()
    conn.close()


def get_or_create_user(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE name = ?", (name,))
    user_id = c.fetchone()
    if user_id:
        return user_id[0]
    c.execute("INSERT INTO users (name, profile) VALUES (?, '{}')", (name,))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def save_profile(user_id, profile_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET profile = ? WHERE id = ?", (json.dumps(profile_data), user_id))
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT profile FROM users WHERE id = ?", (user_id,))
    profile = c.fetchone()[0]
    conn.close()
    return json.loads(profile) if profile else {}

def add_task(user_id, desc, due, status='pending'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, desc, due, status) VALUES (?, ?, ?, ?)", (user_id, desc, due, status))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return task_id

def get_tasks(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, desc, due, status FROM tasks WHERE user_id = ?", (user_id,))
    tasks = c.fetchall()
    conn.close()
    return [{'id': t[0], 'desc': t[1], 'due': t[2], 'status': t[3]} for t in tasks]