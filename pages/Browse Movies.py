# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:09:30 2023

@author: shwet
"""
import streamlit as st
import pandas as pd




def browse(keyword):
    filtered_df = main[main['original_title'].str.contains(keyword, case=False)]
    filtered_df = filtered_df.sort_values(by='weighted_rating', ascending=False)
    final=filtered_df[['original_title', 'genres', 'rating', 'release_date','overview']]
    final=final.head(5)
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
       st.title("Search For Movies")

       keyword=st.text_input("Enter your Keyword : ")
       st.title("Showing Results")
       browse(keyword)
    
   except Exception as e:
        st.error("An error occurred: " + str(e))
    
    


