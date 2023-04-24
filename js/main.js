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
});

//load the old game list in the load game tab
document.querySelector('#load-button').addEventListener('click', async function (evt) {
    evt.preventDefault();
    const target = document.querySelector('#loadGame-ol');
    const response = await fetchData(`${url}save-data/info`);
    for (let session of response) {
        target.innerHTML += '<li> <input type="radio" id="' + session[1] + '" name="choice" value="' + session[1] + '" /> ' +
            '<label for="' + session[1] + '"> ' + session[0] + ' </label> </li>';
    }
});

//actually load the selected save file
document.querySelector('#loadGameMenu-form').addEventListener('submit', async function(evt) {
    evt.preventDefault();
    const gameId = document.querySelector('input[name=choice]:checked').value;
    document.querySelector('#load-game').classList.add('hide');
    await fetchData(`${url}load-game/${gameId}`);
    await gameSetup(url);
});

//main menu functionality
//load the new game tab
document.querySelector('#new-button').addEventListener('click', async function (evt) {
    evt.preventDefault();
    document.querySelector('#main-menu').classList.add('hide');
    document.querySelector('#new-game').classList.remove('hide');
});
//load the old games tab
document.querySelector('#load-button').addEventListener('click', function (evt) {
    evt.preventDefault();
    document.querySelector('#load-game').classList.remove('hide');
    document.querySelector('#main-menu').classList.add('hide');
});

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
            marker.setZIndexOffset(1000);
        }
    }
}

//draw the airports in range
async function airportInRngMarker() {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    const inRange = await fetchData(`${url}airport-in-range/`)
    for (let airport of airports) {
        for (let airportInRange of inRange) {
            if (airportInRange[0] === airport[0]) {
                const marker = L.marker([airport[1], airport[2]], {icon: inRangeIcon}).addTo(map);
                marker.bindPopup(`<b>${airport[0]}<form></form> <input class="flyHere" id="${airport[0]}" 
                type="submit" value="Fly here"></b>`);
                marker.setZIndexOffset(999);
                const popupContent = document.createElement('div');
                const h4 = document.createElement('h4');
                h4.innerHTML = airport[0];
                popupContent.append(h4);
                const goButton = document.createElement('button');
                goButton.classList.add('button');
                goButton.innerHTML = 'Fly here';
                popupContent.append(goButton);
                marker.bindPopup(popupContent);
                goButton.addEventListener('click', async function () {
                    await fetchData(`${url}/movement/${airport[0]}`);
                    console.log(airport[0]);
                    await gameSetup();
                });
            }
        }
    }
}
//fly to new airport


//create the airport markers
async function airportsMarkers() {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    for (let airport of airports) {
            const marker = L.marker([airport[1], airport[2]], {icon: airportIcon}).addTo(map);
            marker.bindPopup(`<b>${airport[0]} </b>`);
    }
}

//right now only creates the markers for all airports and the player
async function gameSetup() {
    try {
        await playerMarker();
        await airportInRngMarker();
        await airportsMarkers()
    } catch (error) {
        console.log(error);
    }
}

//the map
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 50,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([45, -108], 4);
