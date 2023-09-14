# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 19:37:52 2023

@author: shwet
"""

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise.model_selection import RandomizedSearchCV, KFold
from surprise import Reader, Dataset, SVD
import numpy as np

def hybrid_recommend(user_input,user_id):
    input_title = user_input.lower()
    
    # Content-based recommendation
    idx = indices[input_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    content_based = titles.iloc[movie_indices]
    content_based=pd.DataFrame(content_based,columns=['id','title']).reset_index()
    content_based=content_based.drop('id',axis=1)
    content_based = content_based.rename(columns={'index': 'id'})
    colab_ratings=pd.merge(ratings,content_based,left_on='movieId',right_on='id')
    colab_ratings.drop(['id','title'],axis=1,inplace=True)
    lowest_rating = colab_ratings['rating'].min()
    highest_rating = colab_ratings['rating'].max()
    reader = Reader(rating_scale=(lowest_rating, highest_rating))
    data = Dataset.load_from_df(colab_ratings, reader)
 #   similarity_options = {'name': 'cosine', 'user_based': True}
    param_distributions = {'n_factors': np.arange(10, 50, 25), 'n_epochs': np.arange(20, 40, 5)}
    kfold = KFold(n_splits=5, random_state=2023, shuffle=True)
    rs = RandomizedSearchCV(SVD, param_distributions, n_iter=10, measures=['rmse', 'mae'], cv=kfold, random_state=2023)
    rs.fit(data)
    cf_algo = rs.best_estimator['rmse']
    cf_algo.fit(data.build_full_trainset())
    iids = ratings['movieId'].unique()
    u_iid = ratings[ratings['userId'] == user_id]['movieId'].unique()
    iids_to_predict = np.setdiff1d(iids, u_iid)
    testset = [[user_id, iid, 0.] for iid in iids_to_predict]
    predictions = cf_algo.test(testset)
    pred_ratings = np.array([pred.est for pred in predictions])
    collaborative_filtered = pd.DataFrame({'Item_ID': iids_to_predict, 'Exp_Rating': pred_ratings})
    sorted_cf = collaborative_filtered.sort_values(by=['Exp_Rating', 'Item_ID'], ascending=[False, True])
    sorted_cf = pd.merge(sorted_cf, movies, left_on='Item_ID', right_on='id')
    sorted_cf = sorted_cf[['title', 'release_date', 'overview']].head(10)
    for index, row in sorted_cf.iterrows():
            st.write("==================================================================")
            st.write("Original Title:", row['title'])
            st.write("Release Date:", row['release_date'])
            st.write("Overview:", row['overview'])
            st.write("==================================================================")

if __name__ == "__main__":
    try:
        st.title("Hybrid Movie Recommendation")

        user_input = st.text_input("Enter movie title: ")
        user_id = st.text_input("Enter user ID: ")

           
        movies = pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/final_movies.csv')
        ratings = pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/ratings_small.csv')
        ratings.drop('timestamp', axis=1, inplace=True)
        lowest_rating = ratings['rating'].min()
        highest_rating = ratings['rating'].max()
        main = movies
        main['title'] = main['title'].str.lower()
        main['original_title'] = main['original_title'].str.lower()
        main.dropna(subset=['overview'], inplace=True)
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(main['overview'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        titles = main['title']
        indices = pd.Series(main.index, index=main['title'])

 
            
        if user_input and user_id:
            st.title("Showing Results")
            
            recommendations = hybrid_recommend(user_input, int(user_id))
            
            
            
            


    except Exception as e:
        st.error("An error occurred: " + str(e))