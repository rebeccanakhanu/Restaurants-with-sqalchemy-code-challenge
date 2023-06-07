import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant')

    def __repr__(self):
        return f'Restaurant: {self.name}'

    def customers(self):
        return session.query(Customer).join(Review).filter(Review.restaurant_id == self.id).all()


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def __repr__(self):
        return f'Review ID: {self.id}, Rating: {self.star_rating}'

    def full_review(self):
        restaurant_name = self.restaurant.name
        customer_full_name = self.customer.full_name()
        return f"Review for {restaurant_name} by {customer_full_name}: {self.star_rating} stars."


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    reviews = relationship('Review', back_populates='customer')

    def __repr__(self):
        return f'Customer: {self.full_name()}'

    def restaurants(self):
        return session.query(Restaurant).join(Review).filter(Review.customer_id == self.id).all()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
     review = Review(star_rating=rating, restaurant=restaurant)
     self.reviews.append(review)
     session.add(review)


    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                self.reviews.remove(review)
                session.delete(review)
    session.commit()


@classmethod
def fanciest(cls):
    return session.query(cls).order_by(cls.price.desc()).first()


class CustomerRestaurant(Base):
    __tablename__ = 'customer_restaurant'

    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), primary_key=True)


Base.metadata.create_all(engine)
