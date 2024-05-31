import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
import numpy as np
from .models import Rating

def get_recommendations():
    # Retrieve all Rating instances
    ratings_with_products = Rating.objects.all()
    print(ratings_with_products)

    # Convert Rating queryset to a DataFrame
    rating_df = pd.DataFrame(list(ratings_with_products.values('user_id', 'product_id', 'rating')))

    # Rename columns to match the naming convention for Surprise library
    rating_df.rename(columns={'user_id': 'userId', 'product_id': 'productId', 'rating': 'rating'}, inplace=True)

    # Load the data into the Surprise dataset
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(rating_df[['userId', 'productId', 'rating']], reader)

    # Split the data into training and test sets
    trainset, testset = train_test_split(data, test_size=0.25)

    # Train the SVD algorithm
    algo = SVD()
    algo.fit(trainset)

    # Evaluate the algorithm on the test set
    predictions = algo.test(testset)
    accuracy.rmse(predictions)

    return algo, rating_df

def get_top_n_recommendations(user_id, algo, rating_df, n=10):
    # Get a list of all product IDs
    all_product_ids = rating_df['productId'].unique()
    
    # Predict ratings for all products for the given user
    predictions = [algo.predict(user_id, product_id) for product_id in all_product_ids]
    # Sort the predictions by the estimated rating
    top_n_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    
    # Get the product IDs of the top n predictions
    top_n_product_ids = [pred.iid for pred in top_n_predictions]
    
    return top_n_product_ids
