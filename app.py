from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # change this to something secure

# ---------------------- DATABASE CONNECTION ----------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="admin_system"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ---------------------- LOGIN PAGE ----------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()

            if admin:
                session['admin'] = admin['username']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid username or password")
        else:
            return render_template('login.html', error="Database connection failed")

    return render_template('login.html')

# ---------------------- FORGOT PASSWORD ----------------------
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        fullname = request.form['fullname']
        birthdate = request.form['birthdate']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return render_template('forgot_password.html', error="Passwords do not match")

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Check if admin exists with given fullname and birthdate
            cursor.execute(
                "SELECT * FROM admin WHERE fullname=%s AND birthdate=%s",
                (fullname, birthdate)
            )
            admin = cursor.fetchone()

            if admin:
                # Update password
                cursor.execute(
                    "UPDATE admin SET password=%s WHERE id=%s",
                    (new_password, admin['id'])
                )
                conn.commit()
                cursor.close()
                conn.close()
                return render_template('forgot_password.html', success="Password updated successfully!")
            else:
                cursor.close()
                conn.close()
                return render_template('forgot_password.html', error="Admin not found with provided information")
        else:
            return render_template('forgot_password.html', error="Database connection failed")

    return render_template('forgot_password.html')


# ---------------------- RESET PASSWORD ----------------------
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'verified_admin' not in session:
        return redirect(url_for('forgot_password'))

    message = ''
    success = False

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            message = "Passwords do not match."
        else:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE admin SET password=%s WHERE username=%s",
                               (new_password, session['verified_admin']))
                conn.commit()
                cursor.close()
                conn.close()
                message = "Password successfully changed!"
                success = True
                # Clear verified session
                session.pop('verified_admin', None)
            else:
                message = "Database connection failed."

    return render_template('reset_password.html', message=message, success=success)



# ---------------------- LOGOUT ----------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------- DASHBOARD ----------------------
# ---------------------- DASHBOARD ----------------------
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM documents")
        documents = cursor.fetchall()

        cursor.execute("SELECT * FROM residents")
        residents = cursor.fetchall()

        cursor.execute("SELECT * FROM document_requests ORDER BY id DESC")
        requests_data = cursor.fetchall()

        # Count approved certificates (from records)
        cursor.execute("SELECT COUNT(*) AS approved_count FROM records WHERE status = 'Approved'")
        approved_count = cursor.fetchone()['approved_count']

        # ----------------- UPDATED DOUGHNUT CHART DATA -----------------
        certificate_types = [
            "Barangay Clearance",
            "Certificate of Residency",
            "Certificate of Indigency",
            "Certificate of Good Moral Character",
            "Certificate of Appearance",
            "Certificate of No Pending Case",
            "Barangay Business Clearance",
            "Certificate for Solo Parent",
            "Certificate for Senior Citizen",
            "Certificate for Persons with Disabilities (PWD)",
            "Certificate of Guardianship",
            "Certificate of Employment (within Barangay)",
            "Certificate of Low Income",
            "Certificate for Scholarship Application",
            "Certificate for Building/Construction Permit"
        ]

        chart_labels = []
        chart_values = []

        for cert in certificate_types:
            # Only count documents that still exist in the records table
            cursor.execute("SELECT COUNT(*) AS count FROM records WHERE document_type=%s AND status='Approved'", (cert,))
            result = cursor.fetchone()
            chart_labels.append(cert)
            chart_values.append(result['count'] if result else 0)

        # ----------------- MONTHLY REPORT BAR CHART DATA -----------------
        cursor.execute("""
            SELECT MONTH(approved_time) AS month, COUNT(*) AS total 
            FROM records 
            WHERE YEAR(approved_time) = YEAR(CURDATE()) AND status='Approved'
            GROUP BY MONTH(approved_time)
            ORDER BY MONTH(approved_time)
        """)
        doc_monthly = cursor.fetchall()

        cursor.execute("""
            SELECT MONTH(date_registered) AS month, COUNT(*) AS total 
            FROM residents 
            WHERE YEAR(date_registered) = YEAR(CURDATE())
            GROUP BY MONTH(date_registered)
            ORDER BY MONTH(date_registered)
        """)
        res_monthly = cursor.fetchall()

        # Build arrays for 12 months (Jan–Dec)
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        doc_counts = [0]*12
        res_counts = [0]*12

        for d in doc_monthly:
            doc_counts[d['month'] - 1] = d['total']

        for r in res_monthly:
            res_counts[r['month'] - 1] = r['total']

        cursor.close()
        conn.close()

        return render_template(
            'dashboard.html',
            documents=documents,
            residents=residents,
            requests=requests_data,
            approved_count=approved_count,
            chart_labels=chart_labels,
            chart_values=chart_values,
            username=session['admin'],
            months=months,
            doc_counts=doc_counts,
            res_counts=res_counts
        )
    else:
        return "Database connection failed."



# ---------------------- REQUESTS PAGE ----------------------
@app.route('/requests')
def requests_page():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM document_requests ORDER BY status, id DESC")
        requests_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('requests.html', requests=requests_data, username=session['admin'])
    else:
        return "Database connection failed."

# ---------------------- ADD NEW DOCUMENT REQUEST ----------------------
@app.route('/add_request', methods=['POST'])
def add_request():
    if 'admin' not in session:
        return redirect(url_for('login'))

    full_name = request.form['full_name']
    age = request.form['age']
    dob = request.form['dob']
    address = request.form['address']
    occupation = request.form.get('occupation', '')
    document_type = request.form['document_type']

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor(dictionary=True)

    # Check if resident exists
    cursor.execute("SELECT * FROM residents WHERE CONCAT(firstname, ' ', lastname) = %s", (full_name,))
    resident = cursor.fetchone()

    if not resident:
        cursor.close()
        conn.close()
        return "Request declined: Resident not registered."

    # Insert into document_requests table
    cursor.execute("""
        INSERT INTO document_requests 
        (resident_name, age, dob, address, occupation, document_type, status, request_time)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending', %s)
    """, (full_name, age, dob, address, occupation, document_type, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('requests_page'))

# ---------------------- ACCEPT DOCUMENT REQUEST ----------------------
@app.route('/accept_request/<int:request_id>')
def accept_request(request_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM document_requests WHERE id = %s", (request_id,))
        req = cursor.fetchone()

        if req:
            # Update request to Approved
            cursor.execute("UPDATE document_requests SET status='Approved' WHERE id=%s", (request_id,))

            # Record approved request into records
            cursor.execute("""
                INSERT INTO records 
                (resident_name, contact_number, occupation, document_type, approved_time, status)
                VALUES (%s, %s, %s, %s, %s, 'Approved')
            """, (
                req['resident_name'],
                req.get('address', ''),
                req.get('occupation', ''),
                req['document_type'],
                datetime.now()
            ))
            conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('requests_page'))

# ---------------------- RECORDS PAGE ----------------------
@app.route('/records')
def records():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM records ORDER BY approved_time DESC")
        record_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS approved_count FROM records WHERE status='Approved'")
        approved_count = cursor.fetchone()['approved_count']

        cursor.close()
        conn.close()
        return render_template(
            'records.html', 
            records=record_data, 
            approved_count=approved_count,
            username=session['admin']
        )
    else:
        return "Database connection failed."

# ---------------------- VIEW RESIDENTS PAGE ----------------------
@app.route('/residents')
def residents_page():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM residents ORDER BY date_registered DESC")
        residents = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('residents.html', residents=residents, username=session['admin'])
    else:
        return "Database connection failed."

# ---------------------- ADD NEW RESIDENT ----------------------
@app.route('/add_resident', methods=['GET', 'POST'])
def add_resident():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed."

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        contact_number = request.form['contact_number']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO residents (firstname, lastname, address, contact_number)
            VALUES (%s, %s, %s, %s)
        """, (firstname, lastname, address, contact_number))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('residents_page'))

    conn.close()
    return render_template('add_resident.html', username=session['admin'])

# ---------------------- UPDATE RESIDENT INFO ----------------------
@app.route('/update_resident/<int:resident_id>', methods=['GET', 'POST'])
def update_resident(resident_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        contact_number = request.form['contact_number']

        cursor.execute("""
            UPDATE residents 
            SET firstname=%s, lastname=%s, address=%s, contact_number=%s 
            WHERE id=%s
        """, (firstname, lastname, address, contact_number, resident_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('residents_page'))

    cursor.execute("SELECT * FROM residents WHERE id=%s", (resident_id,))
    resident = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update_resident.html', resident=resident, username=session['admin'])

# ---------------------- DELETE RESIDENT ----------------------
@app.route('/delete_resident/<int:resident_id>')
def delete_resident(resident_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM residents WHERE id = %s", (resident_id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('residents_page'))

# ---------------------- CERTIFICATE FORM ----------------------
@app.route('/certificate_form/<int:record_id>')
def certificate_form(record_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM records WHERE id=%s", (record_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()

    if record:
        return render_template('certificate_form.html', record=record, username=session['admin'])
    else:
        return "Record not found."

# ---------------------- DISPLAY CERTIFICATE ----------------------
@app.route('/certificate/<int:record_id>', methods=['POST'])
def certificate(record_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    purpose = request.form['purpose']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM records WHERE id=%s", (record_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()

    if record:
        now = datetime.now()
        return render_template('certificate.html',
                               name=record['resident_name'],
                               purpose=purpose,
                               now=now,
                               username=session['admin'])
    else:
        return "Record not found."

# ---------------------- SEARCH FUNCTION ----------------------
@app.route('/search', methods=['GET'])
def search():
    if 'admin' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            resident_name AS fullname, 
            address AS contact, 
            occupation, 
            document_type, 
            request_time AS date_requested, 
            status
        FROM document_requests
        WHERE resident_name LIKE %s
        ORDER BY request_time DESC
    """, (f"%{query}%",))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('search_results.html', results=results, query=query, username=session['admin'])

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)

