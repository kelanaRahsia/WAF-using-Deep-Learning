from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db_config = {
    'host' : 'localhost',
    'port' : '3306',
    'user' : 'root',
    'password' : '',
    'database' : 'psm_waf'
}

@app.route('/')
def index():
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM request_logs")
    data = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    # print("data:", data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=8089)
