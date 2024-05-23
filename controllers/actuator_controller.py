from flask import Blueprint, request, render_template, redirect, url_for
actuator = Blueprint("actuator",__name__, template_folder="templates")

actuators = {
    "Motor":20,
    "Buzzer":140
}

@actuator.route('/register_actuator')
def register_actuator():
    return render_template('register_actuator.html')

@actuator.route('/add_actuator', methods=['GET', 'POST'])
def add_actuators():
    global actuators
    if request.method == 'POST':
        actuator = request.form['actuator']
        value = request.form['numero']
    else:
        actuator = request.args.get('actuators', None)
        value = request.args.get('numero', None)
    actuators[actuator] = value
    return render_template("actuators.html", devices=actuators)

@actuator.route('/actuators')
def actuatorsHTML():
    global actuators
    return render_template("actuators.html", devices=actuators)

@actuator.route('/del_actuator', methods=['GET','POST'])
def del_actuator():
    global actuators
    if request.method == 'POST':
        actuator = request.form['actuator']
    else:
        actuator = request.args.get('actuator', None)
    actuators.pop(actuator)
    return render_template("actuators.html", devices=actuators)