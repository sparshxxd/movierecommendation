# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 14:47:53 2023

@author: shwet
"""
import streamlit as st
import pandas as pd

    
def genre_recommend(genre):
    main['genres'] = main['genres'].astype(str)
    genre_movies = main[main['genres'].str.contains(genre, case=False)]
    sorted_genre_movies = genre_movies.sort_values(by='weighted_rating', ascending=False)
    final=sorted_genre_movies[['original_title', 'genres', 'rating', 'release_date','overview']]
    final=final.head(5)
    for index, row in final.iterrows():
            st.write("==================================================================")
            st.write("Original Title:", row['original_title'])
            st.write("Release Date:", row['release_date'])
            st.write("Rating:", row['rating'])
            st.write("Overview:", row['overview'])
            st.write("==================================================================")
        

def popular():


    sorted_genre_movies = main.sort_values(by='weighted_rating', ascending=False)
    final=sorted_genre_movies[['original_title', 'genres', 'rating', 'release_date','overview']]
    final=final.head(20)
    for index, row in final.iterrows():
            st.write("==================================================================")
            st.write("Original Title:", row['original_title'])
            st.write("Release Date:", row['release_date'])
            st.write("Rating:", row['rating'])
            st.write("Overview:", row['overview'])
            st.write("==================================================================")
    

if __name__ == "__main__":
    try:
        main = pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/final_movies.csv')
#        main = pd.read_csv('/recommender_App/final_movies.csv')
       
        tab = st.sidebar.radio("Choose a tab:", ["Popularity", "Based on Genre"])
        if tab == "Popularity":
            st.header("Top 20 Popular Movies")
            st.title("Showing Results")
            popular()

        elif tab == "Based on Genre":
            st.header("Top 5 Movies Based On Genre")
            genre=st.selectbox('Pick one', ['Animation','Action','Adventure','Comedy','Crime','Documentary','Drama','Fantasy','History','Horror','Mystery','Romance','Science Fiction','Thriller'])
            st.title("Showing Results")
            genre_recommend(genre)
    except Exception as e:
        st.error("An error occurred: " + str(e))
    
