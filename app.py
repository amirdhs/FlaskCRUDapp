from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, number):
        self.name = name
        self.email = email
        self.number = number


@app.route('/')
def index():
    all_data = Employee.query.all()
    return render_template('index.html', employees=all_data)


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['employeeName']
        email = request.form['employeeEmail']
        number = request.form['employeePhone']

        employee = Employee(name, email, number)
        db.session.add(employee)
        db.session.commit()
        flash("Employee added successfully")
        return redirect(url_for('index'))
    return render_template('add_employee.html')


@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        employee.name = request.form['employeeName']
        employee.email = request.form['employeeEmail']
        employee.number = request.form['employeePhone']
        db.session.commit()
        flash("Employee updated successfully")
        return redirect(url_for('index'))

    return render_template('edit_employee.html', employee=employee)


@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully")
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)