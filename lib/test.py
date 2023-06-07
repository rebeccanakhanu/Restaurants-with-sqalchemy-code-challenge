# Create a restaurant

import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

from models import Restaurant, Review, Customer

    
restaurant1 = Restaurant(name="Pizza Place", price=2)
session.add(restaurant1)
session.commit()

# Create a customer
customer1 = Customer(first_name="John", last_name="Doe")
session.add(customer1)
session.commit()

# Add a review for the restaurant by the customer
review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
session.add(review1)
session.commit()
