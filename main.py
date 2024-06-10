from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    instrument = db.Column(db.String(50))

    def __init__(self, name, position, instrument):
        self.name = name
        self.position = position
        self.instrument = instrument

with app.app_context():
    db.create_all()

@app.route('/')
def about():
    return render_template("index.html")

@app.route('/get_list')
def get_list():
    staff = Employee.query.order_by(Employee.id.desc()).all()
    #response = []
    #for employee in staff:
    #    response.append({
    #    'id': employee.id,
    #    'name': employee.name,
    #    'position': employee.position,
    #    'instrument': employee.instrument
    #    })
    #return jsonify(response)
    return render_template("get_list.html", staff=staff)

@app.route('/get_list/<int:id>')
def get_employee(id):
    employee = Employee.query.get(id)
    return render_template("get_employee.html", employee=employee)

@app.route('/add_employee', methods = ['POST', 'GET'])  #добавление инф. об используемом сотрудником инструменте
def add_employee():
    if request.method == "POST":
        name = request.form['name']
        instrument = request.form['instrument']
        position = request.form['position']

        employee = Employee(name = name, position = position, instrument = instrument)

        try:
            db.session.add(employee)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении сотрудника произошла ошибка"
    else:
        return render_template("add_employee.html")

@app.route('/delete_employee/<int:id>')  #удаление инф. о сотруднике инструменте
def del_employee(id):
    employee = Employee.query.get(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/get_list')
    except:
        return "При удалении сотрудника произошла ошибка"

@app.route('/update_employee/<int:id>', methods=['POST','GET'])  #редактирование инф. о сотруднике инструменте
def update_employee(id):
    employee = Employee.query.get(id)
    if request.method == "POST":
        employee.name = request.form['name']
        employee.position = request.form['position']
        employee.instrument = request.form['instrument']

        try:
            db.session.commit()
            return redirect('/get_list')
        except:
            return "При редактировании сотрудника произошла ошибка"
    else:
        employee = Employee.query.get(id)
        return render_template("employee_update.html", employee=employee)
"""
@app.route('/get_employee/<int:id>')
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'position': employee.position,
            'instrument': employee.instrument
        })
    else:
        return {'error': 'Employee not found'}
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)