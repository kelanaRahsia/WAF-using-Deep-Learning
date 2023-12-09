from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import subprocess
import os 

app = Flask(__name__)
app.secret_key = '123'  

# Database Configuration
db_config = {
    'host' : 'localhost',
    'port' : '3306',
    'user' : 'root',
    'password' : '',
    'database' : 'psm_waf'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # cursor = db.cursor()
    email = request.form['email']
    password = request.form['password']

    cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")  
    user = cursor.fetchone()

    if user:
        # Store user's information in a session
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[4]
        print("session_uid :", session['user_id'])
        print("role:", session['role'])
        return redirect(url_for('dashboard'))
    else:
        return "Invalid login credentials"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Fetch data from the database (replace 'your_query' with your SQL query)
    connection = mysql.connector.connect(**db_config)
    # Initialize search_query with an empty string
    search_query = ""

    print("test1")

    if 'search' in request.args:
        # request.method = 'POST'
        # Handle the search form submission
        search_query = request.args['search']
        print("search_query:", search_query)
        cursor = connection.cursor()

        if session['role'] == 'admin':
            # If the user is an admin, search all books
            cursor.execute("SELECT * FROM book WHERE book_name LIKE %s", (f"%{search_query}%",))
        else:
            # If the user is not an admin, search user-specific books
            cursor.execute("SELECT * FROM book WHERE author IN ('Charles Perraults', 'Khairolr') AND book_name LIKE %s", (f"%{search_query}%",))

        books = cursor.fetchall()
        cursor.close()

    else:
    # If no search query is provided, display all books 
        cursor = connection.cursor()
        if session['role'] == 'admin':
            cursor.execute('SELECT * FROM book')
        else:
            cursor.execute("SELECT * FROM book WHERE author IN ('Charles Perraults', 'Khairolr')")
        books = cursor.fetchall()
        cursor.close()
        connection.close()  # Close the database connection

    if request.method == 'POST':
        note = request.form.get('note')
        result = None

        if note is not None and note.strip():
            try:
                result = subprocess.check_output(['echo', note], stderr=subprocess.STDOUT, text=True)
                return f'Your Note:<br><pre>{result}</pre>'
            except subprocess.CalledProcessError as e:
                return f'Error executing command:<br><pre>{e.output}</pre>'
            result = f'Note: {note}'  # Placeholder code
        else:
            result = 'No note provided.'
        print("result:", result)

    username = session['username']

    # Display user input (search_query) without proper escaping
    return render_template('mukaBukuDashboard.html', books=books, search_query=search_query)


@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form.get('note')
    print("note:",note)

    if note is not None and note.strip():
        try:
            # Use os.popen() to execute the command and capture the output
            command = "echo '" + note + "'"        
            result = os.popen(command).read()       
            print("result:", result)

            # Append the output to the text file
            with open('sample_note.txt', 'a') as file:
                file.write(result + '\n')

            # Read the updated contents of the text file
            with open('sample_note.txt', 'r') as file:
                notes = file.readlines()

            # Display the notes on the webpage
            return render_template('notes.html', notes=notes)

        except Exception as e:
            return f'Error: {str(e)}'
    else:
        return 'No note provided.'


if __name__ == '__main__':
    app.run(debug=True)

