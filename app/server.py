from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Speicherort für Kalibrierungsdaten
CALIBRATION_FILE = "calibration_data.json"

# Standard-Kalibrierungsfaktor
calibration_factor = 0.5

# Lade Kalibrierungsfaktor
def load_calibration():
    global calibration_factor
    try:
        with open(CALIBRATION_FILE, "r") as file:
            data = json.load(file)
            calibration_factor = data.get("calibration_factor", 0.5)
    except FileNotFoundError:
        save_calibration(0.5)

# Speichere Kalibrierungsfaktor
def save_calibration(factor):
    with open(CALIBRATION_FILE, "w") as file:
        json.dump({"calibration_factor": factor}, file)

# Route für das Frontend
@app.route("/")
def index():
    return render_template("index.html", calibration_factor=calibration_factor)

# Route zum Empfangen der Daten vom ESP8266
@app.route("/data", methods=["POST"])
def receive_data():
    global calibration_factor
    data = request.get_json()
    if not data:
        return "Invalid data", 400

    # Verarbeite die Daten
    tds_value = data["tdsValue"]
    temperature = data["temperature"]
    ec_value = data["ecValue"]

    # Speichere die Daten (kann z. B. in einer Datenbank gespeichert werden)
    print(f"TDS: {tds_value}, Temp: {temperature}°C, EC: {ec_value} µS/cm")

    return "Data received", 200

# Route für die Kalibrierung
@app.route("/calibrate", methods=["POST"])
def calibrate():
    global calibration_factor
    data = request.get_json()
    if not data or "calibration_value" not in data:
        return "Invalid data", 400

    calibration_value = data["calibration_value"]
    calibration_factor = 1000.0 / calibration_value
    save_calibration(calibration_factor)

    return jsonify({"message": "Calibration successful", "calibration_factor": calibration_factor})

if __name__ == "__main__":
    load_calibration()
    app.run(host="0.0.0.0", port=5000)
