import sqlite3
import pandas as pd

DB_NAME = 'library.db'
DATASET_FILE = 'D:\\library_management_system\\book_levels.csv'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create Authors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Authors (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE)''')

    # Create Books table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        author_id INTEGER,
                        language_level TEXT,
                        FOREIGN KEY(author_id) REFERENCES Authors(id))''')

    # Create Members table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT UNIQUE)''')

    # Create Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT)''')

    conn.commit()
    conn.close()


def preload_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Load dataset
    dataset = pd.read_csv(DATASET_FILE)

    # Insert authors
    authors = dataset['Author'].unique()
    for author in authors:
        cursor.execute('INSERT OR IGNORE INTO Authors (name) VALUES (?)', (author,))

    # Insert books
    for _, row in dataset.iterrows():
        cursor.execute('SELECT id FROM Authors WHERE name = ?', (row['Author'],))
        author_id = cursor.fetchone()[0]
        cursor.execute('''INSERT OR IGNORE INTO Books (title, author_id, language_level) 
                          VALUES (?, ?, ?)''', 
                       (row['Title'], author_id, row['Language Level']))

    conn.commit()
    conn.close()
