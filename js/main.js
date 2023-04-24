'use strict'
// icons
const airportIcon = L.divIcon({className: 'red-icon'});
const playerIcon = L.divIcon({className: 'player-icon'});
const inRangeIcon = L.divIcon({className: 'inRange-icon'});

// global variables
const url = 'http://127.0.0.1:5000/';

//create a new game after entering name and desired game length
document.querySelector('#newGameMenu-form').addEventListener('submit', async function (evt) {
    evt.preventDefault();
    const playerName = document.querySelector('#menu-input').value;
    const gameLength = document.querySelector('input[name=game_length]:checked').value;
    console.log(gameLength);
    document.querySelector('#new-game').classList.add('hide');
    const gameId = await fetchData(`${url}new-game/${playerName}&${gameLength}`);
    await fetchData(`${url}load-game/${gameId}`);
    await gameSetup(url)


})

//load an old game
document.querySelector('#load-button').addEventListener('click', async function (evt) {
    evt.preventDefault();
    const target = document.querySelector('#loadGame-ol');
    const response = await fetchData(`${url}save-data/info`);
    for (let session of response) {
        target.innerHTML += '<li> <input type="radio" id="' + session[1] + '" name="choice" value="' + session[1] + '" /> ' +
            '<label for="' + session[1] + '"> ' + session[0] + ' </label> </li>';
    }
})

document.querySelector('#loadGameMenu-form').addEventListener('submit', async function() {
    const gameId = document.querySelector('input[name=choice]:checked').value;
    await fetchData(`${url}load-game/${gameId}`);
    await gameSetup(url);
})

document.querySelector('#loadGameMenu-form').addEventListener('submit', async function(evt){
    evt.preventDefault();
    document.querySelector('#load-game').classList.add('hide');
})

//main menu functionality
document.querySelector('#new-button').addEventListener('click', async function (evt) {
    evt.preventDefault();
    document.querySelector('#main-menu').classList.add('hide');
    document.querySelector('#new-game').classList.remove('hide');
})
document.querySelector('#load-button').addEventListener('click', function (evt) {
    evt.preventDefault();
    document.querySelector('#load-game').classList.remove('hide');
    document.querySelector('#main-menu').classList.add('hide');
})

//fetch the json data from the desired url
async function fetchData(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.log(error.message);
    }
}

//Draw the airports and players marker/s on the map
async function playerMarker()  {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    const playerLoc = await fetchData(`${url}locate/0`);

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

//draw the airports in range
async function airportMarker() {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    const inRange = await fetchData(`${url}airport-in-range/`)
    for (let airport of airports) {
        for (let airportInRange of inRange) {
            if (airportInRange[0] === airport[0]) {
                const marker = L.marker([airport[1], airport[2]], {icon: inRangeIcon}).addTo(map);
                marker.bindPopup(`<b>${airport[0]}</b>`);
            }
        }
    }
}

//right now only creates the markers for all airports and the player
async function gameSetup(url) {
    try {
        const airports = await fetchData(`${url}airport/coordinates/all`);
        const inRange = await fetchData(`${url}airport-in-range/`)
        const playerLoc = await fetchData(`${url}locate/0`);

        await playerMarker();
        await airportMarker();




    } catch (error) {
        console.log(error);
    }
}

//gameSetup(url)

//the map
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 50,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([45, -108], 4);
