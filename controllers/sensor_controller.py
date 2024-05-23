from flask import Blueprint, request, render_template, redirect, url_for

sensors = Blueprint("sensors",__name__, template_folder="templates")

sensores = {
'umidade': '12',
'luminosidade': '20',
'temperatura': '24'
}

# @app.route('/sensors')
# def sensors():
#     dic ={'Umidade: ':18, 'Temperatura: ': 23, 'Luminosidade': 26}
#     #sensores = ['Umidade', 'temperatura', 'luminosidade']
#     return render_template("sensors.html", devices=dic)

@sensors.route('/register_sensor')
def register_sensors():
    return render_template("register_sensor.html")

@sensors.route('/add_sensor', methods=['GET','POST'])
def add_sensors():
    global sensores
    if request.method == 'POST':
        sensor = request.form['sensor']
        numero = request.form['numero']
    else:
        sensor = request.args.get('sensor', None)
        numero = request.args.get('numero', None)
    sensores[sensor] = numero
    return render_template("sensor.html", devices=sensores)

@sensors.route('/list_sensors')
def list_sensors():
    global sensores
    return render_template("sensor.html", devices=sensores)


@sensors.route('/remove_sensor')
def remove_sensor():
    return render_template("remove_sensor.html" , devices=sensores)

@sensors.route('/del_sensor', methods=['GET','POST'])
def del_sensor():
    global sensores
    if request.method == 'POST':
        sensor = request.form['sensor']
    else:
        sensor = request.args.get('sensor', None)
    sensores.pop(sensor)
    return render_template("sensor.html", devices=sensores)

