'use strict'
// icons
const airportIcon = L.divIcon({className: 'red-icon'});
const playerIcon = L.divIcon({className: 'player-icon'});

// global variables
const url = 'http://127.0.0.1:5000/';

//new game form

document.querySelector('#menu-form').addEventListener('submit', async function (evt){
    evt.preventDefault();
    const playerName = document.querySelector('#menu-input').value;
    const gameLength = document.querySelector('input[name=game_length]').value;
    document.querySelector('#new-game').classList.add('hide');
    const gameId = await fetchData(`${url}new-game/${playerName}&${gameLength}`);
    console.log(gameId);
    await fetchData(`${url}load-game/${gameId}`);
})
async function fetchData(url) {
    try {
        const response = await fetch(url);
        return  await response.json();
    } catch (error) {
        console.log(error.message);
    }
}

async function gameSetup(url) {
    try {
        const airports = await fetchData(`${url}airport/coordinates/all`);
        //console.log(airports);

        const playerLoc = await fetchData(`${url}locate/0`);
        //console.log(playerLoc);

        for (let airport of airports) {
            if (playerLoc.location === `'${airport[3]}'`) {
                const marker = L.marker([airport[1], airport[2]], {icon: playerIcon}).addTo(map);
                marker.bindPopup(`<b>${airport[0]}</b>`);
            } else {
                const marker = L.marker([airport[1], airport[2]], {icon: airportIcon}).addTo(map);
                marker.bindPopup(`<b>${airport[0]}</b>`);
            }
        }
    }
    catch (error) {
        console.log(error);
    }
}

gameSetup(url)

const map = L.map('map', {tap: false});
    L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 50,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    }).addTo(map);
    map.setView([45, -108], 4);

