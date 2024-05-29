from flask import Flask, jsonify, request
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

@app.route('/get_list', methods=['GET'])
def get_list():
    staff = Employee.query.all()
    response = []
    for employee in staff:
        response.append({
        'id': employee.id,
        'name': employee.name,
        'position': employee.position,
        'instrument': employee.instrument
        })
    return jsonify(response)

@app.route('/add_employee', methods=['POST'])  #добавление инф. об используемом сотрудником инструменте
def add_employee():
    name = request.form['name']
    position = request.form['position']
    instrument = request.form['instrument']
    employee = Employee(name, position, instrument)
    db.session.add(employee)
    db.session.commit()
    return {"success": 'Employee added successfully'}

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



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

