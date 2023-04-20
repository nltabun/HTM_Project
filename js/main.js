'use strict'
// icons
var airportIcon = L.divIcon({className: 'blue-icon'});

async function fetchData(url) {
    try {
        const response = await fetch(url);
        return  await response.json();
    } catch (error) {
        console.log(error.message);
    }
}

async function gameSetup() {
    try {
        const airports = await fetchData('http://127.0.0.1:5000/airport/coordinates/all');
        console.log(airports);

        for (let airport of airports) {
            const marker = L.marker([airport[1], airport[2]], {icon: airportIcon}).addTo(map);
            marker.bindPopup(`<b>${airport[0]}</b>`);
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
    map.setView([45, -108], 4);
