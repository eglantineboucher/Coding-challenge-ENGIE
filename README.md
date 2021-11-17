# Coding-challenge-ENGIE
The aim of this challenge is to calculate how much power each of a multitude of different powerplants need to produce (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources (gas, kerosine), the Pmin and Pmax of each powerplant and the CO2 allowances.

## How to build and launch the API

I built an API using Flask.
It exposes an endpoint /productionplan that accept a POST with a payload (JSON file).

To run it I downloaded and used Postman.
On Postman, one has to choose 'POST' and write an URL with port=8888, the endpoint /productionplan and name=name_of_the_file.json.

Here is an example:
http://127.0.0.1:8888/productionplan?name=payload3.json

The result is a JSON file giving the name and the corresponding load of every power plant.
I made my program so that it takes into account the CO2 allowances.
