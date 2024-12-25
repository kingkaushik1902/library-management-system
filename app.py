from models import init_db, preload_data
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_NAME = 'library.db'

# Initialize and preload data
init_db()
preload_data()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')
#Create New Login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            # Add the user to the Users table
            cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password))

            # Add the user to the Members table
            cursor.execute('INSERT INTO Members (name, email) VALUES (?, ?)', (username, email))

            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Username or email already exists')

    return render_template('register.html')


# Books Page
@app.route('/books', methods=['GET', 'POST'])
def books_page():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Handle Search
    search_query = request.form.get('search', '') if request.method == 'POST' else ''
    language_level = request.args.get('language_level', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    query = '''SELECT Books.id, Books.title, Authors.name, Books.language_level
               FROM Books
               JOIN Authors ON Books.author_id = Authors.id
               WHERE Books.title LIKE ? AND Books.language_level LIKE ?
               LIMIT ? OFFSET ?'''
    cursor.execute(query, (f'%{search_query}%', f'%{language_level}%', per_page, offset))
    books = cursor.fetchall()

    # Get total count for pagination
    cursor.execute('''SELECT COUNT(*) FROM Books WHERE Books.title LIKE ? AND Books.language_level LIKE ?''',
                   (f'%{search_query}%', f'%{language_level}%'))
    total_books = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_books + per_page - 1) // per_page
    return render_template('books.html', books=books, search_query=search_query,
                           language_level=language_level, page=page, total_pages=total_pages)

# Add Member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Members (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('members_page'))
    return render_template('add_member.html')

# Members Page
@app.route('/members', methods=['GET', 'POST'])
def members_page():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Handle Search
    search_query = request.form.get('search', '') if request.method == 'POST' else request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    query = '''SELECT * FROM Members
               WHERE name LIKE ? OR email LIKE ?
               LIMIT ? OFFSET ?'''
    cursor.execute(query, (f'%{search_query}%', f'%{search_query}%', per_page, offset))
    members = cursor.fetchall()

    # Get total count for pagination
    cursor.execute('SELECT COUNT(*) FROM Members WHERE name LIKE ? OR email LIKE ?', 
                   (f'%{search_query}%', f'%{search_query}%'))
    total_members = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_members + per_page - 1) // per_page
    return render_template('members.html', members=members, search_query=search_query, page=page, total_pages=total_pages)


# Delete Member
@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch the member's details before deleting
    cursor.execute('SELECT name FROM Members WHERE id = ?', (member_id,))
    member = cursor.fetchone()

    if not member:
        conn.close()
        return "Member not found.", 404

    member_name = member[0]

    try:
        # Delete the user from the Members table
        cursor.execute('DELETE FROM Members WHERE id = ?', (member_id,))

        # Delete the user from the Users table
        cursor.execute('DELETE FROM Users WHERE username = ?', (member_name,))

        # Log out the user if the deleted member is currently logged in
        if 'user' in session and session['user'] == member_name:
            session.pop('user', None)  # Remove user from session

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error deleting user: {e}")
        return "An error occurred while deleting the user.", 500
    finally:
        conn.close()

    return redirect(url_for('members_page'))

#To Delete Account
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    username = session['user']

    try:
        # Delete the user from the Members table
        cursor.execute('DELETE FROM Members WHERE name = ?', (username,))

        # Delete the user from the Users table
        cursor.execute('DELETE FROM Users WHERE username = ?', (username,))

        # Commit and log out the user
        conn.commit()
        session.pop('user', None)
    except Exception as e:
        conn.rollback()
        print(f"Error deleting account: {e}")
        return "An error occurred while deleting your account.", 500
    finally:
        conn.close()

    return redirect(url_for('home'))


# Edit Member
@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute('UPDATE Members SET name = ?, email = ? WHERE id = ?', (name, email, member_id))
        conn.commit()
        conn.close()
        return redirect(url_for('members_page'))

    cursor.execute('SELECT * FROM Members WHERE id = ?', (member_id,))
    member = cursor.fetchone()
    conn.close()
    return render_template('edit_member.html', member=member)

# Delete Book
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books_page'))

# Edit Book
@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Get updated data from the form
            title = request.form['title']
            author_id = request.form['author_id']
            language_level = request.form['language_level']

            # Update the database
            cursor.execute('''
                UPDATE Books 
                SET title = ?, author_id = ?, language_level = ? 
                WHERE id = ?
            ''', (title, author_id, language_level, book_id))
            conn.commit()
            conn.close()
            return redirect(url_for('books_page'))
        except Exception as e:
            conn.rollback()
            print(f"Error updating book: {e}")
            return "An error occurred while updating the book.", 500

    try:
        # Fetch the current book details for pre-filling the form
        cursor.execute('SELECT * FROM Books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            return "Book not found.", 404

        # Fetch all authors for the dropdown menu
        cursor.execute('SELECT id, name FROM Authors')
        authors = cursor.fetchall()
        conn.close()
        return render_template('edit_book.html', book=book, authors=authors)
    except Exception as e:
        conn.close()
        print(f"Error fetching book: {e}")
        return "An error occurred while fetching the book details.", 500


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Restrict Access to Certain Pages
@app.before_request
def require_login():
    restricted_routes = ['/books', '/members']
    if request.path in restricted_routes and 'user' not in session:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
