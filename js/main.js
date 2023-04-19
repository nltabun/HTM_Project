'use strict'

async function fetchData(url) {                 // asynchronous function is defined by the async keyword
    try {                                               // error handling: try/catch/finally
        const response = await fetch(url);    // starting data download, fetch returns a promise which contains an object of type 'response'
        return  await response.json();          // retrieving the data retrieved from the response object using the json() function
    } catch (error) {
        console.log(error.message);
    }
}

async function gameSetup() {
    try {
        const airports = await fetchData('http://127.0.0.1:5000/airport/coordinates/all');
        console.log(airports);

        for (let airport of airports) {
            const marker = L.marker([airport[1], airport[2]]).addTo(map);
            marker .bindPopup(`<b>${airport[0]}</b>`)
        }
    }
    catch (error) {
        console.log(error);
    }
}

gameSetup()

const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 50,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([45, -100], 4);
