async function getWeather() {
    const city = document.getElementById('city').value;
    if (!city) {
        alert("Please enter a city name!");
        return;
    }

    try {
        const response = await axios.post('http://localhost:8080/weather', 
            { city: city },
            { headers: { 'Content-Type': 'application/json' } }
        );
        
        const data = response.data;
        
        if (data.error) {
            document.getElementById('weatherResult').innerHTML = 
                `<p style="color: red;">${data.error}</p>`;
        } else {
            document.getElementById('weatherResult').innerHTML = `
                <h2>Weather in ${data.City}</h2>
                <p>Temperature: ${data.Temperature}°C</p>
                <p>Description: ${data.Description}</p>
                <p>Humidity: ${data.Humidity}%</p>
                <p>Wind Speed: ${data.WindSpeed} m/s</p>
            `;
        }
    } catch (error) {
        console.error("Error:", error);
        let errorMsg = error.response?.data?.error || "Error fetching weather data. Please check console for details.";
        document.getElementById('weatherResult').innerHTML = 
            `<p style="color: red;">${errorMsg}</p>`;
    }
}