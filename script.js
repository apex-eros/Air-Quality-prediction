function predictAQI() {
    const location = document.getElementById("location").value;
    const time = document.getElementById("time").value;

    // Prepare the data to be sent in the request body
    const requestData = {
        location: location,
        time: time
    };

    // Send location and time data to Flask server
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData) // Convert requestData to JSON string
    })
    .then(response => response.json())
    .then(data => {
        // Display predicted AQI
        const outputDiv = document.getElementById("output");
        outputDiv.innerText = 'Predicted AQI: ${data.predicted_aqi}';
    })
    .catch(error => console.error('Error:', error));
}