#app_controller.py
from flask import Flask, render_template, request
from models.db import db, instance
from controllers.login import login_
from controllers.sensor_controller import sensors
from models.iot.read import Read
from controllers.actuator_controller import actuator
import json
from controllers.reads_controller import read, Read
from flask_mqtt import Mqtt

temperature = 10
humidity = 10
ultrassom = 10
buzzer_string = ""
led_string = ""
local_string = ""

def create_app():

    
    app = Flask(__name__, 
                template_folder="./templates/", 
                static_folder="./static/",
                root_path="./")


    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)


    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe1 = "Umidade/Computistas"
    topic_subscribe2 = "Temperatura/Computistas"
    topic_subscribe3 = "SensorUltrassom/Computistas"
    topic_subscribe4 = "Buzzer/Computistas"
    topic_subscribe5 = "SituBuzzer/ComputistasacaoAmbiente/Computistas"
    topic_subscribe6 = "LedMosquito/Computistas"

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe1)
            mqtt_client.subscribe(topic_subscribe2)
            mqtt_client.subscribe(topic_subscribe3)
            mqtt_client.subscribe(topic_subscribe4)
            mqtt_client.subscribe(topic_subscribe5)
            mqtt_client.subscribe(topic_subscribe6) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")


    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global temperature, humidity, ultrassom
        if(message.topic==topic_subscribe1):
            js = json.loads(message.payload.decode())
            temperature = js
            try:
                with app.app_context():
                    Read.save_read(topic_subscribe1, temperature)
            except:
                pass
        elif(message.topic==topic_subscribe2):
            js = json.loads(message.payload.decode())
            humidity = js
            try:
                with app.app_context():
                    Read.save_read(topic_subscribe2, humidity)
            except:
                pass
        elif(message.topic==topic_subscribe3):
            js = json.loads(message.payload.decode())
            ultrassom = js
        elif(message.topic==topic_subscribe4):
            global buzzer_string
            buzzer_string = message.payload.decode() 
        elif(message.topic==topic_subscribe5):
            global local_string
            local_string = message.payload.decode()
            print("Local: ", local_string)
        elif(message.topic==topic_subscribe6):
            global led_string
            led_string = message.payload.decode()

    app.register_blueprint(login_, url_prefix='/')
    app.register_blueprint(sensors, url_prefix='/')
    app.register_blueprint(actuator, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')

    

    @app.route('/')
    def index():
        return render_template("login.html")
    
    @app.route('/base')
    def base():
        return render_template('base.html')
    
    @app.route('/esp32product')
    def esp32product():
        return render_template('esp32product.html')
    
    @app.route('/login')
    def userlogin():
        return render_template('login.html')
    
    @app.route('/loginAdmin')
    def loginAdmin():
        return render_template('loginAdmin.html')
    
    @app.route('/baseAdmin')
    def baseAdmin():
        return render_template('baseAdmin.html')
    
    @app.route('/temperaturaHumidade')
    def temperaturaHumidade():
        return render_template('temperaturaUmidade.html')
    
    @app.route('/list_sensors')
    def list_sensors():
        return render_template('sensor.html')
    
    @app.route('/register_sensor')
    def register_sensor():
        return render_template("register_sensor.html")
    
    @app.route('/add_user')
    def list_user():
        return render_template('user.html')
    
    @app.route('/register_user')
    def register_user():
        return render_template('register_user.html')
    
    @app.route('/actuators')
    def list_actuators():
        return render_template('actuators.html')
    
    @app.route('/register_actuator')
    def register_actuator():
        return render_template('register_actuator.html')
    
    @app.route('/temporeal')
    def temporeal():
        global temperature, humidity
        values = {"temperature":temperature, "humidity":humidity}
        return render_template("temporeal.html", values=values)
    
    @app.route('/temporeal_ultrassom')
    def temporeal_ultrassom():
        global ultrassom    
        values={"ultrassom":ultrassom}
        return render_template("temporeal_ultrassom.html", values=values)
    
    @app.route('/temporeal_buzzer')
    def temporeal_buzzer():
        global buzzer_string
        values={"buzzer":buzzer_string}
        return render_template("temporeal_buzzer.html", values=values)
    
    @app.route('/temporeal_led')
    def temporeal_led():
        global led_string
        values={"led":led_string}
        return render_template("temporeal_led.html", values=values)
    
    @app.route('/temporeal_local')
    def temporeal_local():
        global local_string
        values={"local":local_string}
        return render_template("temporeal_local.html", values=values)
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    
    
    return app