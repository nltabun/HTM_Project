'use strict'
// regions
const airportIcon = L.divIcon({className: 'red-icon'});
const playerIcon = L.divIcon({className: 'player-icon'});
const inRangeIcon = L.divIcon({className: 'inRange-icon'});

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

//load the players data
async function playerData() {
    const playerData = await fetchData(`${url}refresh-player-data`); //fetch the player data

    let name = document.querySelector('#name');
    name.innerText = playerData.name;

    let stock = document.querySelector('#stock');
    stock.innerText = playerData.money;

    let AP = document.querySelector('#actionpoints');
    AP.innerText = playerData.ap;

    let range = document.querySelector('#range');
    range.innerText = Math.round(playerData.range);

    let fuel = document.querySelector('#fuel');
    fuel.innerText = `${playerData.fuelCurrent} / ${playerData.fuelCapacity}`;

     let fuelStorage = document.querySelector('#fuelStorage');
    fuelStorage.innerText = playerData.fuelReserve;

    if (playerData.ap <= 0) {
        document.querySelector('#fuelForm').classList.add('hide');
        document.querySelector('#miniForm').classList.add('hide');
        document.querySelector('#clue-form').classList.add('hide');
        const game_end = await fetchData(`${url}/end-turn`);

        document.querySelector('#alerts').classList.remove('hide');
        if (game_end.status === 0) {
            alert.innerText = 'Musk found his car, you LOSE';
        } else {
            document.querySelector('#alerts').classList.remove('hide');
            alert.innerText = 'Your turn has ended \n Starting new Round';
        }
        await gameSetup();
    }
}

//open the minigame menu
document.querySelector('#action-minigame').addEventListener('click', async function(evt) {
    evt.preventDefault();
    let alert = document.querySelector('#alerts-p');
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');

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
                document.querySelector("[id=" + CSS.escape(id1) +"]").value = answer;
                document.querySelector("[id=" + CSS.escape(label) +"]").innerHTML = answer;
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
                alert.innerText = `Your answer was correct, you earned ${result.prize} stock`;
            }else {
                alert.innerText = `Your answer was incorrect. Better luck next time.`;
            }
            await gameSetup();
    });

//open the fuel menu
document.querySelector('#action-fuel').addEventListener('click', function() {
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#fuelForm').classList.remove('hide');
});

//buy or load fuel
document.querySelector('#fuelForm').addEventListener('submit', async function(evt) {
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
        }else {
            alert.innerText = `You cannot afford that much fuel.`;
        }
    }
});

//buy a clue thing idk at this point
document.querySelector('#action-clue').addEventListener('click', function() {
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    document.querySelector('#clue-form').classList.remove('hide');
    document.querySelector('#clue-button').classList.remove('hide');

    let clue_p = document.querySelector('#clue-p');
    clue_p.innerText = "";
});

//confirm clue purchase and give the clue
document.querySelector('#confirm-clue').addEventListener('click', async function (evt) {
    evt.preventDefault();
    document.querySelector('#clue-button').classList.add('hide');
    const clue = await fetchData(`${url}/clues`);
    let clue_p = document.querySelector('#clue-p');

    if (clue.status === 0) {
        clue_p.innerText = "You dont have enough money or you've already bought your clue this round";
    } else {
        switch (clue.clueType) {
            case 1:
                clue_p.innerText = `Elon Musk is ${clue.clue} of you`;
                break;
            case 2:
                clue_p.innerText = "Elon musk is in this region";
                //TODO if else shit for the map region images
                break;
            case 3:
                clue_p.innerText = "Elon musk is in one these airports:";
                break;
        }
    }
    await gameSetup();
});

//end round button
document.querySelector('#action-end').addEventListener('click', async function () {
    let alert = document.querySelector('#alerts-p');
    document.querySelector('#clue-button').classList.add('hide');
    document.querySelector('#clue-form').classList.add('hide');
    document.querySelector('#fuelForm').classList.add('hide');
    document.querySelector('#miniForm').classList.add('hide');
    const game_end = await fetchData(`${url}/end-turn`);
    if (game_end.status === 0) {
        alert.innerText = 'Musk found his car, you LOSE';
    } else {
        document.querySelector('#alerts').classList.remove('hide');
        alert.innerText = 'Your turn has ended \n Starting new Round';
    }
    await gameSetup();
});

//remove the alert
document.querySelector('#alerts').addEventListener('click', function () {
    document.querySelector('#alerts').classList.add('hide');
    let alert = document.querySelector('#alerts-p');
    alert.innerText = '';
});

//Draw the airports markers on the map
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
                    const game_end = await fetchData(`${url}/movement/${airport.ident}`);
                    console.log(`${url}movement/${airport.ident}`);

                    document.querySelector('#alerts').classList.remove('hide');
                        if (game_end.status === 2) {
                            document.querySelector('#alerts').classList.add('hide');
                            let alert = document.querySelector('#alerts-p');
                            alert.innerText = 'You found Elon Musk! You WON the game!';
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


