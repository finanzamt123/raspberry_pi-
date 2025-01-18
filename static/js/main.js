const serverUrl = "http://localhost:5000";

// Elemente für die Anzeige
const tdsValueElement = document.getElementById("tdsValue");
const temperatureElement = document.getElementById("temperature");
const calibrateButton = document.getElementById("calibrate");

// Funktion zum Abrufen der aktuellen Daten
async function fetchData() {
  try {
    const response = await fetch(`${serverUrl}/data`);
    if (response.ok) {
      const data = await response.json();
      tdsValueElement.textContent = data.tdsValue.toFixed(2);
      temperatureElement.textContent = data.temperature.toFixed(2);
    } else {
      console.error("Fehler beim Abrufen der Daten:", response.status);
    }
  } catch (error) {
    console.error("Netzwerkfehler:", error);
  }
}

// Funktion zur Kalibrierung
async function calibrate() {
  try {
    const response = await fetch(`${serverUrl}/calibrate`, { method: "POST" });
    if (response.ok) {
      alert("Kalibrierung erfolgreich!");
    } else {
      alert("Fehler bei der Kalibrierung.");
    }
  } catch (error) {
    alert("Netzwerkfehler bei der Kalibrierung.");
    console.error(error);
  }
}

// Eventlistener für den Kalibrierungsbutton
calibrateButton.addEventListener("click", calibrate);

// Automatische Aktualisierung alle 5 Sekunden
setInterval(fetchData, 5000);

// Initiales Laden der Daten
fetchData();
