from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector  # Use mysql.connector for MySQL

app = Flask(__name__)
app.secret_key = "yoursecretkey"  # Needed for flash messages

# -----------------------------
# MySQL Connection Function
# -----------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ClassX2025@!",  # Replace with your MySQL root password
            database="classx_db"      # Your database name
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# -----------------------
# Home route
# -----------------------
@app.route('/')
def home():
    return render_template('home.html', title='Home')

# -----------------------
# Enroll Page (GET + POST)
# -----------------------
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
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

        # Save to Database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
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
# Other routes
# -----------------------
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

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

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
