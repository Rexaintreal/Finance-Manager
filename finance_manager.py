from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('user.txt', 'a') as file:
            file.write(f'{username},{password}\n')
        session['username'] = username  # set session key for new user
        return redirect(url_for('form'))
    return render_template('register.html')

# Function to get financial information for a given username
def get_financial_info(username):
    with open('financial_info.txt', 'r') as f:
        for line in f:
            fields = line.strip().split(',')
            if fields[0] == username:
                return [float(x) for x in fields[1:]]
    return None

# Function to write financial information to file for a given username
def write_to_file(username, monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses):
    with open('financial_info.txt', 'a') as file:
        file.write(f"{username},{monthly_income},{housing_expenses},{transportation_expenses},{food_expenses},{other_expenses}\n")
    financial_info = get_financial_info(username)
    if financial_info:
        monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses = financial_info
        return render_template('dashboard.html', monthly_income=monthly_income, housing_expenses=housing_expenses,
                               transportation_expenses=transportation_expenses, food_expenses=food_expenses,
                               other_expenses=other_expenses)


# Function to save financial information to file
def save_financial_info():
    if request.method == 'POST':
        username = session['username']
        monthly_income = request.form['monthly_income']
        housing_expenses = request.form['housing_expenses']
        transportation_expenses = request.form['transportation_expenses']
        food_expenses = request.form['food_expenses']
        other_expenses = request.form['other_expenses']
        
        write_to_file(username, monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('user.txt', 'r') as file:
            for line in file:
                if line.strip() == f'{username},{password}':
                    session['username'] = username  # store the username in the session object
                    financial_info = get_financial_info(username)
                    if financial_info:
                        return redirect(url_for('dashboard'))
                    else:
                        return redirect(url_for('form'))
        return redirect(url_for('register'))
    return render_template('login.html')

# Form route
@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        monthly_income = request.form['monthly_income']
        housing_expenses = request.form['housing_expenses']
        transportation_expenses = request.form['transportation_expenses']
        food_expenses = request.form['food_expenses']
        other_expenses = request.form['other_expenses']
        
        write_to_file(username, monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses)
        
    financial_info = get_financial_info(username)
    if financial_info:
        monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses = financial_info
        return render_template('form.html', monthly_income=monthly_income, housing_expenses=housing_expenses,
                               transportation_expenses=transportation_expenses, food_expenses=food_expenses,
                               other_expenses=other_expenses)

    return render_template('form.html')


# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    financial_info = get_financial_info(username)

    if request.method == 'POST':
        save_financial_info()
        return redirect(url_for('dashboard'))

    if financial_info:
        monthly_income, housing_expenses, transportation_expenses, food_expenses, other_expenses = financial_info
        return render_template('dashboard.html', monthly_income=monthly_income, housing_expenses=housing_expenses,
                                transportation_expenses=transportation_expenses, food_expenses=food_expenses,
                                other_expenses=other_expenses)
    else:
        return redirect(url_for('form'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

