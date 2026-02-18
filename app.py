from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import math

app = Flask(__name__)
DB_FILE = 'jobs.db'
ITEMS_PER_PAGE = 5  # Jobs per page

# Initialize database if it doesn't exist
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database created!")

init_db()

# Helper to get filtered, sorted, paginated jobs
def get_jobs(search="", status_filter="", sort_by="", page=1):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    # Search
    if search:
        query += " AND (company LIKE ? OR role LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # Status filter
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    # Sorting
    if sort_by in ['company', 'role', 'status']:
        query += f" ORDER BY {sort_by} COLLATE NOCASE"

    # Execute
    c.execute(query, params)
    all_jobs = c.fetchall()
    total_jobs = len(all_jobs)
    total_pages = max(1, math.ceil(total_jobs / ITEMS_PER_PAGE))

    # Pagination slice
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    jobs_page = all_jobs[start:end]

    conn.close()
    return jobs_page, page, total_pages

# Home page
@app.route('/')
def home():
    search = request.args.get('search', '')
    status_filter = request.args.get('status_filter', '')
    sort_by = request.args.get('sort_by', '')
    page = int(request.args.get('page', 1))

    jobs, page, total_pages = get_jobs(search, status_filter, sort_by, page)
    return render_template('index.html', jobs=jobs, page=page, total_pages=total_pages, search=search, status_filter=status_filter, sort_by=sort_by)

# Add job
@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        status = request.form['status']

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO jobs (company, role, status) VALUES (?, ?, ?)", (company, role, status))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('add_job.html')

# Update job
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_job(id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        status = request.form['status']
        c.execute("UPDATE jobs SET company = ?, role = ?, status = ? WHERE id = ?", (company, role, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    c.execute("SELECT * FROM jobs WHERE id = ?", (id,))
    job = c.fetchone()
    conn.close()
    return render_template('update_job.html', job=job)


# Delete job
@app.route('/delete/<int:id>', methods=['POST'])
def delete_job(id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

