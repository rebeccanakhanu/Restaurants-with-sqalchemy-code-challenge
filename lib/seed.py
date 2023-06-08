from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from models import Review, Restaurant, Customer, customer_restaurants
if __name__ == "__main__":
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Customer).delete()
    fake = Faker()
    customers = []
    for _ in range(20):
        customer = Customer(
            first_name=fake.first_name()
        )
        session.add(customer)
        customers.append(customer)
    restaurants = []
    for _ in range(20):
        restaurant = Restaurant(
            name=fake.company(),
            price=random.randint(200, 500)
        )
        session.add(restaurant)
        restaurants.append(restaurant)
    existing_combinations = set()
    for _ in range(50):
        customer_id = random.randint(1, 20)
        restaurant_id = random.randint(1, 20)
        if (customer_id, restaurant_id) in existing_combinations:
            continue
        existing_combinations.add((customer_id, restaurant_id))
        customer_restaurant_data = {"customer_id": customer_id, "restaurant_id": restaurant_id}
        stmt = insert(customer_restaurants).values(customer_restaurant_data)
        session.execute(stmt)
    for _ in range(50):
        review = Review(
            star_rating=random.randint(1, 5),
            customer_id=random.randint(1, 20),
            restaurant_id=random.randint(1, 20)
        )
        session.add(review)
    session.commit()
    session.close()