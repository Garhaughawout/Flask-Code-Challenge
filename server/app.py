#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return ""

class Restaurants(Resource):
    def get(self):
        restaurants = [resturant.to_dict() for resturant in Restaurant.query.all()]

        return make_response(restaurants, 200)

    
api.add_resource(Restaurants, "/restaurants")


class RestaurantsbyId(Resource):
    
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        
        if restaurant is None:
            return make_response({"error": "Restaurant not found"}, 404)
        
        return make_response(restaurant.to_dict(), 200)
    
    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).one_or_none()
        
        if restaurant is None:
            return make_response({"error": "Restaurant not found"}, 404)
        
        db.session.delete(restaurant)
        db.session.commit()
        
        return make_response({}, 204)
    
api.add_resource(RestaurantsbyId, "/restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        
        return make_response(pizzas, 200)
    
api.add_resource(Pizzas, "/pizzas")

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        
        try: 
            restaurantpizza = RestaurantPizza(
                restaurant_id=data['restaurant_id'], 
                pizza_id=data['pizza_id'],
                price=data['price']
                )
            db.session.add(restaurantpizza)
            db.session.commit()
            return make_response(restaurantpizza.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
            
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
