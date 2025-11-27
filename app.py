from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import re  

def is_valid_email(email):
     
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    
    return phone.isdigit() and len(phone) >= 7

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ClassX2025@!",   
            database="classx_db"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

app = Flask(__name__)
app.secret_key = "yoursecretkey"   
 
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
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))    
        else:
            flash("Incorrect email or password!", "danger")

    return render_template('login.html', title='Login')
 
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))
 
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if 'user_id' not in session:
        flash("Please login to enroll!", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    
    if request.method == 'POST':
         
        first_name = request.form.get('first_name') if not user['first_name'] else user['first_name']
        last_name = request.form.get('last_name') if not user['last_name'] else user['last_name']
        phone = request.form.get('phone') if not user['phone'] else user['phone']
 
        course = request.form.get('course')
        experience = request.form.get('experience')
        motivation = request.form.get('motivation')
        newsletter = 1 if request.form.get('newsletter') else 0

        try:
            
            cursor.execute("""
                UPDATE users 
                SET first_name=%s, last_name=%s, phone=%s
                WHERE id=%s
            """, (first_name, last_name, phone, session['user_id']))

            
            cursor.execute("""
                INSERT INTO enrollments (user_id, course, experience, motivation, newsletter)
                VALUES (%s, %s, %s, %s, %s)
            """, (session['user_id'], course, experience, motivation, newsletter))

            conn.commit()
            flash("Enrollment successful!", "success")
            return redirect(url_for('dashboard'))

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    
    cursor.execute("SELECT * FROM enrollments WHERE user_id=%s", (session['user_id'],))
    enrollments = cursor.fetchall()
    total_courses = len(enrollments)

    cursor.close()
    conn.close()


    return render_template('enroll.html', title='Enroll', user=user, enrollments=enrollments, total_courses=total_courses)
 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
 
    cursor.execute("SELECT * FROM enrollments WHERE user_id=%s", (session['user_id'],))
    enrollments = cursor.fetchall()
   
    total_courses = len(enrollments)

    cursor.close()
    conn.close()

    return render_template('dashboard.html', title="Dashboard", user=user, enrollments=enrollments, total_courses=total_courses)



@app.route('/course')
def course():
    return render_template('course.html', title="My Courses")

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
         
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        
        if not all([first_name, last_name, email, phone, password, confirm_password]):
            flash("Please fill in all required fields!", "warning")
            return redirect(url_for('signup'))

         
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        
        if not is_valid_email(email):
            flash("Invalid email format!", "danger")
            return redirect(url_for('signup'))

     
        if not is_valid_phone(phone):
            flash("Invalid phone number!", "danger")
            return redirect(url_for('signup'))

        
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            existing = cursor.fetchone()

            if existing:
                flash("Email already exists!", "warning")
                return redirect(url_for('signup'))

             
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, email, phone, password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")

        finally:
            cursor.close()
            conn.close()

    
    return render_template('signup.html', title='Sign Up')


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
