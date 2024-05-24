from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    last_report = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/devices/active')
def active_devices():
    threshold = datetime.utcnow() - timedelta(minutes=30)
    active_devices = Device.query.filter(Device.last_report >= threshold).all()
    return jsonify([device.imei for device in active_devices])

@app.route('/api/devices/inactive-with-status')
def inactive_devices():
    threshold = datetime.utcnow() - timedelta(minutes=30)
    inactive_devices = Device.query.filter(Device.last_report < threshold).all()
    result = []
    for device in inactive_devices:
        status = 'inactive'
        if device.last_report < datetime.utcnow() - timedelta(hours=24):
            status = 'critical'
        elif device.last_report < datetime.utcnow() - timedelta(hours=12):
            status = 'warning'
        result.append({'imei': device.imei, 'status': status})
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def device_status():
    threshold_inactive = datetime.utcnow() - timedelta(minutes=30)
    threshold_warning = datetime.utcnow() - timedelta(hours=12)
    threshold_critical = datetime.utcnow() - timedelta(hours=24)

    power_on_count = Device.query.filter(Device.status == 'poweron').count()
    power_off_count = Device.query.filter(Device.status == 'poweroff').count()
    inactive_count = Device.query.filter(Device.status == 'inactive', Device.last_report < threshold_inactive).count()
    warning_count = Device.query.filter(Device.last_report < threshold_warning, Device.last_report >= threshold_critical).count()
    critical_count = Device.query.filter(Device.last_report < threshold_critical).count()

    app.logger.info(f"PowerOn Count: {power_on_count}")
    app.logger.info(f"PowerOff Count: {power_off_count}")
    app.logger.info(f"Inactive Count: {inactive_count}")
    app.logger.info(f"Warning Count: {warning_count}")
    app.logger.info(f"Critical Count: {critical_count}")

    return jsonify({
        'powerOnCount': power_on_count,
        'powerOffCount': power_off_count,
        'inactiveCount': inactive_count,
        'warningCount': warning_count,
        'criticalCount': critical_count
    })

@app.route('/api/critical-count', methods=['GET'])
def critical_count():
    threshold_critical = datetime.utcnow() - timedelta(hours=24)
    critical_count = Device.query.filter(Device.last_report < threshold_critical).count()
    return jsonify({'criticalCount': critical_count})

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.get_json()
    app.logger.info(f"Received data: {data}")

    if not isinstance(data, list):
        app.logger.error("Invalid data format. Expected a list of dictionaries.")
        return jsonify({"error": "Invalid data format. Expected a list of dictionaries."}), 400

    for entry in data:
        if not isinstance(entry, dict):
            app.logger.error(f"Invalid entry format: {entry}. Expected a dictionary.")
            return jsonify({"error": f"Invalid entry format: {entry}. Expected a dictionary."}), 400

        required_keys = {'imei', 'status', 'last_report_minutes_ago'}
        if not required_keys.issubset(entry.keys()):
            app.logger.error(f"Missing keys in entry: {entry}. Required keys: {required_keys}")
            return jsonify({"error": f"Missing keys in entry: {entry}. Required keys: {required_keys}"}), 400

        imei = entry['imei']
        status = entry['status']
        last_report = datetime.utcnow() - timedelta(minutes=entry['last_report_minutes_ago'])

        app.logger.info(f"Updating/adding device with IMEI: {imei}, Status: {status}, Last Report: {last_report}")

        device = Device.query.filter_by(imei=imei).first()
        if device:
            device.status = status
            device.last_report = last_report
        else:
            new_device = Device(imei=imei, status=status, last_report=last_report)
            db.session.add(new_device)
    
    db.session.commit()
    app.logger.info("Data added/updated successfully")
    return jsonify({"message": "Data added/updated successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
