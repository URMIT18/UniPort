from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configure database connection
DB_NAME = 'test'
DB_USER = 'postgres'
DB_PASSWORD = '4486'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Connect to the database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query_course = request.form.get('search_query_course', '')
        search_query_state = request.form.get('search_query_state', '')
        
        if 'clear_search' in request.form:
            return render_template('index.html', data=[], search_query_course=None, search_query_state=None)

        cursor = conn.cursor()
        query = f"SELECT * FROM uploaded_data WHERE \"Course\" ~* %s AND \"State\" ~* %s"
        cursor.execute(query, (search_query_course, search_query_state))
        data = cursor.fetchall()
        cursor.close()
        return render_template('index.html', data=data, search_query_course=search_query_course, search_query_state=search_query_state)
    else:
        return render_template('index.html', data=[], search_query_course=None, search_query_state=None)
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
