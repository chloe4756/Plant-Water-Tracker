const weatherKey = "208381d7aab77fad49b49cf9bdf6ccf7";
const weatherUrl = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=";
const searchBox = document.querySelector(".weatherInput");
const searchBtn = document.querySelector(".weatherBtn");



main();
function main(){

    let  weather = [];



    addListeners();
function addListeners() {
    searchBtn.addEventListener("click", function () {
        checkWeather(searchBox.value);
    });
}

async function checkWeather(city) {
    const response = await fetch(weatherUrl + city + `&appid=${weatherKey}`);
    var data = await response.json();
    if (data.weather && data.weather.length > 0) {
        let weatherDescp = data.weather[0].description;
        document.querySelector(".temp").innerHTML = `<p>Current Weather: ${weatherDescp}</p>`;
        checkRain(weatherDescp);
    } else {
        document.querySelector(".temp").innerHTML = `<p>City not found or invalid. Please try again.</p>`;
    }
}



function checkRain(weather) {
        if (weather === "thunderstorm with light rain" || weather === "thunderstorm with rain" || 
        weather === "thunderstorm with heavy rain" || weather === "thunderstorm with heavy rain" || 
        weather === "light thunderstorm" || weather === "thunderstorm" || 
        weather === "heavy thunderstorm" || weather === "ragged thunderstorm" || 
        weather === "thunderstorm with light drizzle" || weather === "thunderstorm with drizzle" || 
        weather === "thunderstorm with heavy drizzle" || weather === "light intensity drizzle" || 
        weather === "drizzle" || weather === "heavy intensity drizzle" || 
        weather === "light intensity drizzle rain" || weather === "drizzle rain" || 
        weather === "heavy intensity drizzle rain" || weather === "shower rain and drizzle" || 
        weather === "heavy shower rain and drizzle" || weather === "shower drizzle" || 
        weather === "light rain" || weather === "moderate rain" || 
        weather === "heavy intensity rain" || weather === "very heavy rain" || 
        weather === "extreme rain" || weather === "freezing rain" || 
        weather === "light intensity shower rain" || weather === "shower rain" || 
        weather === "heavy intensity shower rain" || weather === "ragged shower rain")
        document.querySelector(".waterRecc").innerHTML = `<p>We recommend you to water all your outdoor plants</p>`;
}
}
