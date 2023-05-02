'use strict'
// regions
const airportIcon = L.divIcon({className: 'red-icon'});
const playerIcon = L.divIcon({className: 'player-icon'});
const inRangeIcon = L.divIcon({className: 'inRange-icon'});
const clueAirports = L.divIcon({className: 'clueAirport'});

//the map
const map = L.map('map', {tap: false});
L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    maxZoom: 50,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([45, -108], 4);

// global variables
const url = 'http://127.0.0.1:5000/';
const layerGroup = L.layerGroup().addTo(map);

async function delGame() {
    await fetchData(`${url}game-end`);
    window.location.reload();
}

//create a new game after entering name and desired game length
document.querySelector('#newGameMenu-form').addEventListener('submit', async function (evt) {
    evt.preventDefault();
    const playerName = document.querySelector('#menu-input').value;
    const gameLength = document.querySelector('input[name=game_length]:checked').value;
    console.log(gameLength);
    document.querySelector('#new-game').classList.add('hide');
    const gameId = await fetchData(`${url}new-game/${playerName}&${gameLength}`);
    await fetchData(`${url}load-game/${gameId.id}`);
    await gameSetup(url)
});

//load the old game list in the load game tab
document.querySelector('#load-button').addEventListener('click', async function (evt) {
    evt.preventDefault();
    const target = document.querySelector('#loadGame-ol');
    const response = await fetchData(`${url}save-data/info`);
    for (let session of response) {
        target.innerHTML += '<li> <input type="radio" class="options" id="' + session[1] + '" name="choice" value="' + session[1]
            + '" /> ' + '<label for="' + session[1] + '"> ' + session[0] + ' </label> </li>';
    }
});

//actually load the selected save file
document.querySelector('#loadGameMenu-form').addEventListener('submit', async function (evt) {
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

//load the players data
async function playerData() {
    const playerData = await fetchData(`${url}refresh-player-data`); //fetch the player data
    const weatherData = await fetchData(`${url}weather/${playerData.location}`);

    let name = document.querySelector('#name');
    name.innerText = playerData.name;

    let stock = document.querySelector('#stock');
    stock.innerText = playerData.money;

    let AP = document.querySelector('#actionpoints');
    AP.innerText = playerData.ap;

    let currentPlane = document.querySelector('#plane');
    currentPlane.innerText = playerData.plane;

    let range = document.querySelector('#range');
    range.innerText = Math.round(playerData.range);

    let fuel = document.querySelector('#fuel');
    fuel.innerText = `${playerData.fuelCurrent} / ${playerData.fuelCapacity}`;

    let fuelStorage = document.querySelector('#fuelStorage');
    fuelStorage.innerText = playerData.fuelReserve;

    let temp = document.querySelector('#temp');
    temp.innerText = Math.round(weatherData.temperature);

    let weather_desc = document.querySelector('#weather-desc');
    weather_desc.innerText = weatherData.weather_desc;

    let wind = document.querySelector('#wind-speed');
    wind.innerText = weatherData.wind_speed;

    let visib = document.querySelector('#visibility');
    visib.innerText = weatherData.visibility;

    if (playerData.ap <= 0) {
        document.querySelector('#planeForm').classList.add('hide');
        document.querySelector('#planeComparison').classList.add('hide');
        document.querySelector('#fuelForm').classList.add('hide');
        document.querySelector('#miniForm').classList.add('hide');
        document.querySelector('#clue-form').classList.add('hide');
        document.querySelector('#south').classList.add('hide');
        document.querySelector('#west').classList.add('hide');
        document.querySelector('#northeast').classList.add('hide');
        document.querySelector('#north').classList.add('hide');
        document.querySelector('#can').classList.add('hide');
        document.querySelector('#mex').classList.add('hide');
        const game_end = await fetchData(`${url}/end-turn`);
        await fetchData(`${url}save-game`);

        if (game_end.status === 0) {
            document.querySelector('#alerts').classList.remove('hide');
            alert.innerText = 'Musk found his car, you LOSE. Game closes in 10 seconds';
            setTimeout(delGame, 10000);
        } else {
            document.querySelector('#alerts').classList.remove('hide');
            alert.innerText = 'Your turn has ended \n Starting new Round';
        }
        await gameSetup();
    }
}

//open the minigame menu
document.querySelector('#action-minigame').addEventListener('click', async function (evt) {
    evt.preventDefault();
    let alert = document.querySelector('#alerts-p');
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#planeForm').classList.add('hide');
    document.querySelector('#planeComparison').classList.add('hide');
    document.querySelector('#south').classList.add('hide');
    document.querySelector('#west').classList.add('hide');
    document.querySelector('#northeast').classList.add('hide');
    document.querySelector('#north').classList.add('hide');
    document.querySelector('#can').classList.add('hide');
    document.querySelector('#mex').classList.add('hide');

    const playerData = await fetchData(`${url}refresh-player-data`); //fetch the player data
    if (playerData.minigameDone === 1) {
        document.querySelector('#alerts').classList.remove('hide');
        alert.innerText = `You've already done a minigame this round`;
    } else {
        document.querySelector('#miniForm').classList.remove('hide');
        console.log(playerData.minigameDone);
        let gameData = await fetchData(`${url}minigame/play`)
        const question = document.querySelector('#question');
        question.innerHTML = gameData.question;
        let i = 1;
        document.querySelector('#passIt').title = gameData.id;
        for (let answer of gameData.answers) {
            let id1 = 'a' + i;
            let label = 'aa' + i;
            //console.log(id1);
            document.querySelector("[id=" + CSS.escape(id1) + "]").value = answer;
            document.querySelector("[id=" + CSS.escape(label) + "]").innerHTML = answer;
            i++;
        }
    }
});

//submitting the answer to minigame question
document.querySelector('#miniForm').addEventListener('submit', async function(evt) {
    evt.preventDefault();
    let alert = document.querySelector('#alerts-p');
    document.querySelector('#miniForm').classList.add('hide');
    const qId = document.querySelector("#passIt").title;
    const answer = document.querySelector('input[name=choice1]:checked').value;
    const result = await fetchData(`${url}minigame/answer/${qId}=${answer}`);

    document.querySelector('#alerts').classList.remove('hide');
    if (result.status === 1) {
        alert.innerText = `Your answer was correct, you earned ${result.prize} stocks.`;
    } else if (result.status === -1) {
        alert.innerText = `Your answer was incorrect, you also lost ${result.prize} stocks.`;
    } else {
        alert.innerText = `Your answer was incorrect. Better luck next time.`;
    }
    await gameSetup();
});

//open the fuel menu

document.querySelector('#action-fuel').addEventListener('click', function() {
    document.querySelector('#planeForm').classList.add('hide');
    document.querySelector('#planeComparison').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#south').classList.add('hide');
    document.querySelector('#west').classList.add('hide');
    document.querySelector('#northeast').classList.add('hide');
    document.querySelector('#north').classList.add('hide');
    document.querySelector('#can').classList.add('hide');
    document.querySelector('#mex').classList.add('hide');
    document.querySelector('#fuelForm').classList.remove('hide');
});

//buy or load fuel
document.querySelector('#fuelForm').addEventListener('submit', async function (evt) {
    evt.preventDefault();
    const playerData = await fetchData(`${url}refresh-player-data`);
    let buy_load = document.querySelector('input[name=buy-load]:checked').value;

    let how_much;
    if (buy_load === 'max') {
        let max_fuel = playerData.fuelCapacity - playerData.fuelCurrent;
        if (playerData.fuelReserve > max_fuel) {
            how_much = max_fuel;
        } else {
            how_much = playerData.fuelReserve;
        }
        buy_load = 'load';
    } else {
        how_much = document.querySelector('#how-much').value;
    }
    console.log(how_much, buy_load);
    console.log(`${url}fuel-management/${buy_load}=${how_much}`);
    document.querySelector('#fuelForm').classList.add('hide');
    const fuel = await fetchData(`${url}fuel-management/${buy_load}=${how_much}`);
    await gameSetup();

    document.querySelector('#alerts').classList.remove('hide');
    let alert = document.querySelector('#alerts-p');
    const spent = fuel.oldMoney - fuel.newMoney;

    if (buy_load === 'load') {
        if (how_much > playerData.fuelReserve) {
            alert.innerText = `You do not have that much fuel in reserve.`;
        } else {
            alert.innerText = `You loaded ${how_much} fuel into your plane.`;
        }
    } else {
        if (fuel.success === true) {
            alert.innerText = `You bought ${how_much} fuel, it cost you ${spent} stock.`;
        } else {
            alert.innerText = `You cannot afford that much fuel.`;
        }
    }
});

//open the plane browser
document.querySelector('#action-plane').addEventListener('click', async function(evt) {
    evt.preventDefault();
    const list = document.querySelector('#planeForm-ol');
    const current = document.querySelector('#currentPlane');
    list.innerHTML = '';

    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#planeComparison').classList.add('hide');
    document.querySelector('#planeForm').classList.remove('hide');
    document.querySelector('#south').classList.add('hide');
    document.querySelector('#west').classList.add('hide');
    document.querySelector('#northeast').classList.add('hide');
    document.querySelector('#north').classList.add('hide');
    document.querySelector('#can').classList.add('hide');
    document.querySelector('#mex').classList.add('hide');

    const planes = await fetchData(`${url}planes/browse`);
    let i = 0;
    for (let plane of planes.planes) {
        if (planes.currentPlaneIdx === plane.index) {
            current.innerHTML += `<td> Current plane: ${plane.name} 
                                 <br> fuel capacity: ${plane.fuelCapacity}
                                 <br> fuel efficiency: ${plane.fuelEfficiency}
                                 <br> speed: ${plane.speed} </td>`;
        } else {
            if (i === 0) {
                list.innerHTML += `<li> <input type="radio" name="bruh" id="${plane.index}" value="${plane.index}" checked="checked"> <label for="${plane.index}">
                                 name: ${plane.name}
                            <br> fuel capacity: ${plane.fuelCapacity} 
                            <br> fuel efficiency: ${plane.fuelEfficiency}
                            <br> speed: ${plane.speed}
                            <br> cost: ${plane.cost} </label></li>`;
            } else {
                list.innerHTML += `<li> <input type="radio" name="bruh" id="${plane.index}" value="${plane.index}"> <label for="${plane.index}">
                                 name: ${plane.name}
                            <br> fuel capacity: ${plane.fuelCapacity} 
                            <br> fuel efficiency: ${plane.fuelEfficiency}
                            <br> speed: ${plane.speed}
                            <br> cost: ${plane.cost} </label></li>`;
            }
           i++;
        }
    }
});

//plane comparison
document.querySelector('#planeForm').addEventListener('submit', async function(evt) {
    evt.preventDefault();
    document.querySelector('#planeForm').classList.add('hide');
    document.querySelector('#planeComparison').classList.remove('hide');

    const compPlaneId = document.querySelector('input[name=bruh]:checked').value;
    const planes = await fetchData(`${url}planes/browse`);
    const comparisonData = await fetchData(`${url}planes/compare/${planes.currentPlaneIdx}=${compPlaneId}`);

    const currentPlane = document.querySelector('#currentPlane2');
    const stats = document.querySelector('#stats');
    const comparablePlane = document.querySelector('#comparedPlane');

    currentPlane.innerHTML = `<p>Current plane: 
                              <br>name: ${comparisonData.old_plane.name} 
                              <br>fuel capacity: ${comparisonData.old_plane.fuelCapacity} 
                              <br> fuel efficiency: ${comparisonData.old_plane.fuelEfficiency}
                              <br> speed: ${comparisonData.old_plane.speed}</p>`;
    stats.innerText = `Stat differences: (positive = better, negative = worse) 
                      \n fuel capacity: ${comparisonData.new_plane.fuelCapacity - comparisonData.old_plane.fuelCapacity} 
                      \n fuel efficiency: ${Math.round((comparisonData.new_plane.fuelEfficiency - comparisonData.old_plane.fuelEfficiency) * 10) / 10} 
                      \n speed: ${comparisonData.new_plane.speed - comparisonData.old_plane.speed} 
                      \n new plane cost: ${comparisonData.cost} stock`;
    comparablePlane.innerHTML = `<p>New plane: 
                                <br>name: ${comparisonData.new_plane.name} 
                                <br>fuel capacity: ${comparisonData.new_plane.fuelCapacity} 
                                <br> fuel efficiency: ${comparisonData.new_plane.fuelEfficiency}
                                <br> speed: ${comparisonData.new_plane.speed}</p>`;

    document.querySelector('#planeComparison').addEventListener('submit', async function(evt){
        evt.preventDefault();
        document.querySelector('#planeComparison').classList.add('hide');
        let alert = document.querySelector('#alerts-p');
        document.querySelector('#alerts').classList.remove('hide');
        const bruh = await fetchData(`${url}planes/buy=${compPlaneId}`);
        if(bruh.status === 0) {
            alert.innerText = 'Something went wrong with your purchase';
        }else {
            alert.innerText = 'Your purchase was successful';
        }
        await gameSetup();
    });
});

//buy a clue thing idk at this point
document.querySelector('#action-clue').addEventListener('click', function () {
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#planeForm').classList.add('hide');
    document.querySelector('#planeComparison').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#south').classList.add('hide');
    document.querySelector('#west').classList.add('hide');
    document.querySelector('#northeast').classList.add('hide');
    document.querySelector('#north').classList.add('hide');
    document.querySelector('#can').classList.add('hide');
    document.querySelector('#mex').classList.add('hide');
    document.querySelector('#clue-form').classList.remove('hide');
    document.querySelector('#clue-button').classList.remove('hide');

    let clue_p = document.querySelector('#clue-p');
    clue_p.innerText = "";
});

//confirm clue purchase and give the clue
document.querySelector('#confirm-clue').addEventListener('click', async function (evt) {
    evt.preventDefault();
    let doneSetup = 0;
    document.querySelector('#clue-button').classList.add('hide');
    const clue = await fetchData(`${url}clues`);
    let clue_p = document.querySelector('#clue-p');

    if (clue.status === 0) {
        clue_p.innerText = "You dont have enough money or you've already bought your clue this round";
    } else {
        switch (clue.clueType) {
            case 1:
                clue_p.innerText = `Elon Musk is ${clue.clue} of you`;
                break;
            case 2:
                if (clue.clue === 'NEA') {
                    document.querySelector('#northeast').classList.remove('hide');
                } else if (clue.clue === 'STH') {
                    document.querySelector('#south').classList.remove('hide');
                } else if (clue.clue === 'MDW') {
                    document.querySelector('#north').classList.remove('hide');
                } else if (clue.clue === 'PAC') {
                    document.querySelector('#west').classList.remove('hide');
                } else if (clue.clue === 'CAN') {
                    document.querySelector('#can').classList.remove('hide');
                } else if (clue.clue === 'MCA') {
                    document.querySelector('#mex').classList.remove('hide');
                }
                break;
            case 3:
                clue_p.innerText = "Elon musk is in one these airports highlighted in purple (disappears in 10 seconds)";
                for (let airport of clue.clue) {
                    if (Array.isArray(airport[2])) {
                        const array = airport[2];
                        const marker = L.marker([array[0], array[1]], {icon: clueAirports}).addTo(map);
                        marker.bindPopup(`<b>${airport[0]}</b>`);
                        marker.setZIndexOffset(1000);
                        marker.addTo(layerGroup);
                    } else {
                        const marker = L.marker([airport[2], airport[3]], {icon: clueAirports}).addTo(map);
                        marker.bindPopup(`<b>${airport[0]}</b>`);
                        marker.setZIndexOffset(1000);
                        marker.addTo(layerGroup);

                        doneSetup = 1;
                    }
                }
        }
    }

    function bruh() {
        gameSetup();
    }

    if (doneSetup === 1) {
        await playerData();
        setTimeout(bruh, 10000);
    } else {
        await gameSetup();
    }
});

//hide the map clue
document.querySelector('#south').addEventListener('click', function () {
    document.querySelector('#south').classList.add('hide');
});

document.querySelector('#west').addEventListener('click', function () {
    document.querySelector('#west').classList.add('hide');
});

document.querySelector('#northeast').addEventListener('click', function () {
    document.querySelector('#northeast').classList.add('hide');
});

document.querySelector('#north').addEventListener('click', function () {
    document.querySelector('#north').classList.add('hide');
});

document.querySelector('#can').addEventListener('click', function () {
    document.querySelector('#can').classList.add('hide');
});

document.querySelector('#mex').addEventListener('click', function () {
    document.querySelector('#mex').classList.add('hide');
});

//end round button
document.querySelector('#action-end').addEventListener('click', async function () {
    let alert = document.querySelector('#alerts-p');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#planeForm').classList.add('hide');
    document.querySelector('#planeComparison').classList.add('hide');
    document.querySelector('#south').classList.add('hide');
    document.querySelector('#west').classList.add('hide');
    document.querySelector('#northeast').classList.add('hide');
    document.querySelector('#north').classList.add('hide');
    document.querySelector('#can').classList.add('hide');
    document.querySelector('#mex').classList.add('hide');
    
    const game_end = await fetchData(`${url}/end-turn`);
    if (game_end.status === 0) {
        alert.innerText = 'Musk found his car, you LOSE. Game closes in 10 seconds';
        setTimeout(delGame, 10000);
    } else {
        document.querySelector('#alerts').classList.remove('hide');
        alert.innerText = 'Your turn has ended \n Starting new Round';
    }
    await fetchData(`${url}save-game`);
    await gameSetup();
});

//remove the alert
document.querySelector('#alerts').addEventListener('click', function () {
    document.querySelector('#alerts').classList.add('hide')
    let alert = document.querySelector('#alerts-p');
    alert.innerText = '';
});

//Draw the players marker on the map
async function playerMarker()  {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    const playerLoc = await fetchData(`${url}locate/0`);

    let playerAirport = document.querySelector('#player-location');
    playerAirport.innerText = playerLoc.name;

    for (let airport of airports) {
        if (playerLoc.name === airport.name) {
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {icon: playerIcon}).addTo(map);
            marker.bindPopup(`<b>${airport.name}</b>`);
            marker.setZIndexOffset(1000);
            marker.addTo(layerGroup);
        }
    }
}

//draw the airports in range and have the option to move into them.
async function airportInRngMarker() {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    const inRange = await fetchData(`${url}airport-in-range/`);
    for (let airport of airports) {
        for (let airportInRange of inRange) {
            if (airportInRange.name === airport.name) {
                const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {icon: inRangeIcon}).addTo(map);
                marker.bindPopup(`<b>${airport.name}<form></form> <input class="flyHere" id="${airport.name}" 
                type="submit" value="Fly here"></b>`);
                marker.setZIndexOffset(999);
                const popupContent = document.createElement('div');
                const h4 = document.createElement('h4');
                h4.innerHTML = `${airport.name} <br> costs: ${airportInRange.apCost} ap`;
                popupContent.append(h4);
                const goButton = document.createElement('button');
                goButton.classList.add('button');
                goButton.innerHTML = 'Fly here';
                popupContent.append(goButton);
                marker.bindPopup(popupContent);
                marker.addTo(layerGroup);
                goButton.addEventListener('click', async function () {
                    const game_end = await fetchData(`${url}movement/${airport.ident}`);
                    const event = await fetchData(`${url}location-events`);

                    document.querySelector('#south').classList.add('hide');
                    document.querySelector('#west').classList.add('hide');
                    document.querySelector('#northeast').classList.add('hide');
                    document.querySelector('#north').classList.add('hide');
                    document.querySelector('#can').classList.add('hide');
                    document.querySelector('#mex').classList.add('hide');

                    if (event.status === 1) {
                        let alert = document.querySelector('#alerts-p');
                        alert.innerText = event.message;
                    }
                    if (game_end.status === 2) {
                        document.querySelector('#alerts').classList.remove('hide');
                        let alert = document.querySelector('#alerts-p');
                        alert.innerText = 'You found Elon Musk! You WON the game! Game closes in 10 seconds';
                        setTimeout(delGame, 10000);
                    }
                    await gameSetup(url);
                });
            }
        }
    }
}

//create the airport markers
async function airportsMarkers() {
    const airports = await fetchData(`${url}airport/coordinates/all`);
    for (let airport of airports) {
        const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {icon: airportIcon}).addTo(map);
        marker.bindPopup(`<b>${airport.name} </b>`);
        marker.addTo(layerGroup);
    }
}

//right now only creates the markers for all airports and the player
async function gameSetup() {
    try {
        layerGroup.clearLayers();
        await playerData();
        await airportsMarkers()
        await playerMarker();
        await airportInRngMarker();

    } catch (error) {
        console.log(error);
    }
}

//Goes back to main menu from new game
document.querySelector('#back-button').addEventListener('click', function (evt) {
    evt.preventDefault();
    document.querySelector('#new-game').classList.add('hide');
    document.querySelector('#main-menu').classList.remove('hide');
});
//Goes back to main menu from load game
document.querySelector('#back-button2').addEventListener('click', function (evt) {
    evt.preventDefault();
    document.querySelector('#load-game').classList.add('hide');
    document.querySelector('#main-menu').classList.remove('hide');
});
