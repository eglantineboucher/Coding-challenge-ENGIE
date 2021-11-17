# Coding-challenge-ENGIE
The aim of this challenge is to calculate how much power each of a multitude of different powerplants need to produce (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources (gas, kerosine), the Pmin and Pmax of each powerplant and the CO2 allowances.

## A little bit more on the API

To create my API I used the Flask framework and to try it I downloaded and used Postman.<p>
This API contains just one endpoint: productionplan. To create this endpoint, I defined a Python class and connected it to the desired endpoint:
```php
class ProductionPlan(Resource):
  #program 
  
api.add_resource(ProductionPlan, '/productionplan')  # '/productionplan' is our entry point
```

Inside this class, I included the POST method that allowed me to add a JSON file to my program. This argument is passed to my API endpoint as URL parameter, which look like this:<br>
http://127.0.0.1:8888/productionplan?name=payload3.json <p>

Then, I specified the required parameters and parsed the values provided using `reqparse` like this: <br>
```php
def post(self):
        #adding a file called name (eg of an URL: http://127.0.0.1:8888/productionplan?name=payload3.json)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        
        #creating a variable new_data which is the file given
        new_data=args.name
```
Here, I also created new_data from the URL parameter args which will be the file my code will take as an input to run.

## How to launch the API?

To run the API, the first step is to host it: <br>
```php
if __name__ == '__main__':
    app.run(port=8888)  # run our Flask app on the 8888 port
```
<p>
Then, when running the script we get this message:<br>
 
![image](https://user-images.githubusercontent.com/47385060/142242336-4b285f8e-aa40-48b2-b241-8a342dffcb34.png)
<br>
This means the server is set up, the next step requires Postman.<p>
  
On Postman, I choose the POST request (upper left corner) to my localhost adress (eg: http://127.0.0.1:8888) through the endpoint `/productionplan` and taking an URL parmeter `name=payload1.json`. Clicking on the SEND button (upper right corner) gives the json file on the lower half of the picture with the answer to the challenge.<br>
![image](https://user-images.githubusercontent.com/47385060/142241438-9f9df45d-cf3d-4d05-8982-d6ec2f01a423.png)<br>
