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