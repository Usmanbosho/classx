from flask import Flask, render_template, request, redirect, url_for, flash, session

import mysql.connector
import re  # for simple email validation


# -----------------------
# Helper Functions
# -----------------------
def is_valid_email(email):
    # Basic email regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    # Basic phone validation (numbers only, min 7 digits)
    return phone.isdigit() and len(phone) >= 7

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ClassX2025@!",  # Replace with your MySQL root password
            database="classx_db"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

app = Flask(__name__)
app.secret_key = "yoursecretkey"  # Needed for session and flash


# -----------------------
# Home Route
# -----------------------
@app.route('/')
def home():
    total_students = 0
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM enrollments")
            total_students = cursor.fetchone()[0]  # Get the count
        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('home.html', title='Home', total_students=total_students)


# -----------------------
# Login Route (GET + POST)
# -----------------------
# -----------------------
# Login Route (GET + POST)
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']  # password

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM enrollments WHERE email=%s AND phone=%s", (email, phone))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['student_id'] = user['id']
            session['student_name'] = user['first_name']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or phone number!", "danger")

    return render_template('login.html', title='Login')



# -----------------------
# Logout Route
# -----------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

# -----------------------
# Enroll Page (GET + POST)
# -----------------------
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    # if 'user_id' not in session:
    #     flash("Please login to enroll!", "warning")
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        # Capture all form fields
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form.get('phone')
        course = request.form['course']
        education = request.form.get('education')
        experience = request.form.get('experience')
        motivation = request.form.get('motivation')
        schedule = request.form.get('schedule')
        newsletter = 1 if request.form.get('newsletter') else 0

        # Check if email or phone already exists
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM enrollments WHERE email=%s OR phone=%s", (email, phone))
                existing = cursor.fetchone()
                if existing:
                    flash("Email or phone number already enrolled!", "warning")
                else:
                    cursor.execute("""
                        INSERT INTO enrollments
                        (first_name, last_name, email, phone, course, education, experience, motivation, schedule, newsletter)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (first_name, last_name, email, phone, course, education, experience, motivation, schedule, newsletter))
                    conn.commit()
                    flash("Enrollment successful!", "success")
            except mysql.connector.Error as e:
                flash(f"Database Error: {e}", "danger")
            finally:
                cursor.close()
                conn.close()

        return redirect(url_for('enroll'))

    return render_template('enroll.html', title='Sign Up')

# -----------------------
# Other Routes
# -----------------------
# -----------------------
# Student Dashboard
# -----------------------
@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))
    # Fetch student info from DB
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM enrollments WHERE id=%s", (session['student_id'],))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', title="Dashboard", student=student)

@app.route('/course')
def course():
    return render_template('course.html', title="My Courses")

# @app.route('/enroll')
# def enroll():
#     return render_template('enroll.html', title="Enroll New Course")

@app.route('/profile')
def profile():
    return render_template('profile.html', title="Profile")

@app.route('/certificates')
def certificates():
    return render_template('certificates.html', title="Progress & Certificates")

@app.route('/messages')
def messages():
    return render_template('messages.html', title="Messages")

@app.route('/support')
def support():
    return render_template('support.html', title="Support")

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/404')
def not_found():
    return render_template('404.html', title='Page Not Found')

@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')

@app.route('/blog-details')
def blog_details():
    return render_template('blog-details.html', title='Blog Details')

@app.route('/course-details')
def course_details():
    return render_template('course-details.html', title='Course Details')

@app.route('/courses')
def courses():
    return render_template('courses.html', title='Courses')

@app.route('/events')
def events():
    return render_template('events.html', title='Events')

@app.route('/instructor-profile')
def instructor_profile():
    return render_template('instructor-profile.html', title='Instructor Profile')

@app.route('/instructors')
def instructors():
    return render_template('instructors.html', title='Instructors')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

@app.route('/starter-page')
def starter_page():
    return render_template('starter-page.html', title='Starter Page')

@app.route('/terms')
def terms():
    return render_template('terms.html', title='Terms & Conditions')


if __name__ == '__main__':
    app.run(debug=True)
