from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuator import Actuator

write = Blueprint("write",__name__, template_folder="views")


@write.route("/history_write")
def history_write():
    actuator = Actuator.get_actuator()
    write = {}
    return render_template("history_write.html", actuator = actuator, write = write)

@write.route("/get_write", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)
        actuator = Actuator.get_actuator()
        return render_template("history_write.html", actuator = actuator, write = write)