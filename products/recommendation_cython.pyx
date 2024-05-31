# recommendation_cython.pyx

import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
cimport cython

def get_recommendations():
    from .models import Rating  # Import Django models inside the function to avoid cyclic imports

    # Retrieve all Rating instances
    ratings_with_products = Rating.objects.all()

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

cpdef list get_top_n_recommendations(int user_id, algo, rating_df, int n=10):
    cdef list all_product_ids = rating_df['productId'].unique().tolist()
    cdef list predictions = []
    cdef int i
    cdef int length = len(all_product_ids)

    for i in range(length):
        product_id = all_product_ids[i]
        pred = algo.predict(user_id, product_id)
        predictions.append(pred)
    
    predictions.sort(key=lambda x: x.est, reverse=True)

    cdef list top_n_product_ids = []
    cdef int limit = min(n, length)
    for i in range(limit):
        top_n_product_ids.append(predictions[i].iid)
    
    return top_n_product_ids
