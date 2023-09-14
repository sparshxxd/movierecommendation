# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:04:28 2023

@author: shwet
"""
#-------------------------------Collaborative Filtering------------------------
#Loading libraries
import streamlit as st
import numpy as np 
import pandas as pd
from surprise.model_selection import RandomizedSearchCV
from surprise.model_selection.split import KFold
import surprise
import warnings; warnings.simplefilter('ignore')


# Now you can import modules from that folder

def movie_for_user(user):
    iids = ratings['movieId'].unique()
    u_iid = ratings[ratings['userId'] == user]['movieId'].unique()
    iids_to_predict = np.setdiff1d(iids, u_iid)
    testset = [[user, iid, 0.] for iid in iids_to_predict]
    
    # Get predictions for the current user
    predictions = algo.test(testset)
    pred_ratings = np.array([pred.est for pred in predictions])
    
    exp_ratings = pd.DataFrame({'Item_ID': iids_to_predict, 'Exp_Rating': pred_ratings})
    sorted_exp = exp_ratings.sort_values(by=['Exp_Rating', 'Item_ID'], ascending=[False, True])
    sorted_exp = pd.merge(sorted_exp, movies, left_on='Item_ID', right_on='id')
    sorted_exp = sorted_exp[['original_title', 'release_date', 'overview']].head(5)
    return sorted_exp

def show(df):
    for index, row in df.iterrows():
            st.write("==================================================================")
            st.write(index+1)
            st.write("Original Title:", row['original_title'])
            st.write("Release Date:", row['release_date'])
            st.write("Overview:", row['overview'])
            st.write("==================================================================")
    

if __name__ == "__main__":
    try:
        st.title("User Based Recommender")

        user_input=st.text_input("Enter user id: ")
        st.write("Recommending for User: 564,547,15,73,452,528,519,20,36,361 ")


        if user_input:
            user = int(user_input)
     
            movies=pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/final_movies.csv')
            ratings = pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/ratings_small.csv') 
            
            ratings.drop('timestamp', axis=1, inplace=True) 
            rating_name = pd.merge(ratings, movies, left_on='movieId', right_on='id', how='inner')
            rating_name.drop_duplicates(['userId','original_title'],inplace=True)
            rating_new=rating_name[['userId','movieId','rating_x']]
            lowest_rating = rating_new['rating_x'].min()
            highest_rating = rating_new['rating_x'].max()
            
            reader = surprise.Reader(rating_scale = (lowest_rating,highest_rating))
            data = surprise.Dataset.load_from_df(rating_new,reader)
            similarity_options = {'name': 'cosine', 'user_based': True}
            # Define the parameter distributions for RandomizedSearchCV
            param_distributions = {'n_factors': np.arange(10, 50, 25), 'n_epochs': np.arange(20, 40, 5)}
                    
            # Define KFold cross-validation
            kfold = KFold(n_splits=5, random_state=2023, shuffle=True)
                    
            # Create RandomizedSearchCV object
            rs = RandomizedSearchCV(surprise.SVD, param_distributions, n_iter=10, measures=['rmse', 'mae'], cv=kfold, random_state=2023)
            rs.fit(data)
            #'rmse': 0.8888, 'mae': 0.6868
            algo = rs.best_estimator['rmse']
            algo.fit(data.build_full_trainset())
            st.title("Showing Results")
            df=movie_for_user(user)
            show(df)
    
    except Exception as e:
        st.error("An error occurred: " + str(e))
        
    
