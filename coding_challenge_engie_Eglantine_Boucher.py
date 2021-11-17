# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:27:26 2021

@author: eggy
"""
from  scipy import *
from  pylab import *

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import json

########################################################################################
#function to find the minimum price of each power plant and add it in feature
def minimum_price(data):
    feature=data['powerplants']
    for k in range (len(feature)):
        
        #adding minimum price = 0 for windturbines
        if feature[k]['type']=='windturbine':
            feature[k]['minimum_price'] = 0
        
        #adding minimum price for kerosine
        elif feature[k]['type']=='turbojet':
            feature[k]['minimum_price'] = data['fuels']['kerosine(euro/MWh)']/(feature[k]['efficiency'])
    
        #adding minimum price for gasfired taking into account Pmin and co2 allowances
        elif feature[k]['type']=='gasfired':
            feature[k]['minimum_price'] = feature[k]['pmin']*(data['fuels']['gas(euro/MWh)']+0.3*data['fuels']['co2(euro/ton)'])/(feature[k]['efficiency'])
    return(feature)
    
#######################################################################################
#function to sort by increasing minimum_price the feature table
def sort(data):
    feature=minimum_price(data)
    for i in range(1, len(feature)):
        
        current_position = i
        current_element = feature[i]
        
        #iteration until it reaches first element or the current element is smaller than the previous one
        while current_position > 0 and current_element['minimum_price'] < feature[current_position-1]['minimum_price']:
            
            #change position
            feature[current_position] = feature[current_position-1]
            current_position -= 1
        
        #updating current element
        feature[current_position] = current_element
    return(feature)

#######################################################################################
#function to dispatch the load following on the sorting order found by the function sort
def load_attribution(data):
    feature=sort(data)
    load = data['load']
    
    #initialization of variables
    name_total = []
    p_total = []
    p=0
    
    for j in range (len(feature)):
        #if the load has been totally dispatched the next values will all be 0
        if load == 0:
            p = 0
            
        else:    
            #adding load for windturbines
            if feature[j]['type'] == 'windturbine':
                p = feature[j]['pmax']*data['fuels']['wind(%)']/100
                #if the p is too hign it takes the value of the remaining load
                if p > load:
                    p = load
            
            #adding load for gasfired or turbojet
            elif feature[j]['type'] == 'gasfired' or feature[j]['type'] == 'turbojet':
                p = feature[j]['pmax']
                #if the p is too hign it takes the value of the remaining load
                if p > load:
                    p = load
            
            #updating load    
            load = load - p
            
        #adding corresponding p and name to the output
        name_total.append(feature[j]['name'])
        p_total.append(round(p,1))
        
        
    return(p_total,name_total)
 
#########################################################################################    
#function that gives a json file as an output with the name and the corresponding load of each plant
def response(data):
    response={}
    (p,name)=load_attribution(data)
    for k in range (len(p)):
        response[k]={
                'name': name[k],
                'p': p[k]}
    #saving response as a json file
    with open('response.json', 'w') as mon_fichier:
        json.dump(response, mon_fichier)
    #reading the json file as an output
    with open('response.json') as f:
        final = json.loads(f.read())
    return(final)
    

#########################################################################################
#########################################################################################


app = Flask(__name__)
api = Api(app)


#API creation

class ProductionPlan(Resource):
    
    def post(self):
        #adding a file called name (eg of an URL: http://127.0.0.1:8888/productionplan?name=payload3.json)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        
        #creating a variable new_data which is the file given
        new_data=args.name
        
        with open(new_data) as f:
            data = json.loads(f.read())
        #running all the functions above
        output=response(data)
        return {'data': output}, 200  # return data and 200 OK code
        
        
api.add_resource(ProductionPlan, '/productionplan')  # '/productionplan' is our entry point

if __name__ == '__main__':
    app.run(port=8888)  # run our Flask app on the 8888 port
    