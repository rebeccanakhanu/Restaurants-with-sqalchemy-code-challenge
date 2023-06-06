from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Review, Restaurant, Customer

engine = create_engine('sqlite:///db/restaurants.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create instances of Review
review1 = Review(star_rating=4)
review2 = Review(star_rating=5)

# Add reviews to restaurants and customers
restaurant1 = session.query(Restaurant).first()
customer1 = session.query(Customer).first()

restaurant1.reviews.append(review1)
customer1.reviews.append(review2)

# Commit the changes to the database
session.commit()

