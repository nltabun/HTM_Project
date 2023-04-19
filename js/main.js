'use strict'

async function asynchronousFunction() {                 // asynchronous function is defined by the async keyword
    console.log('asynchronous download begins');
    try {                                               // error handling: try/catch/finally
        const response = await fetch('http://127.0.0.1:5000/airport/coordinates/all');    // starting data download, fetch returns a promise which contains an object of type 'response'
        const coordinateData = await response.json();          // retrieving the data retrieved from the response object using the json() function
        console.log(coordinateData);    // log the result to the console
    } catch (error) {
        console.log(error.message);
    }
}

asynchronousFunction();


const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 50,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([45, -108], 4);
