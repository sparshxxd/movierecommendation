import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
import warnings; warnings.simplefilter('ignore')


def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

def result(input) :
        h=get_recommendations(input).head()
        pd.DataFrame(h)  
        ans = pd.merge(h,main,left_on='title',right_on='original_title')
        ans = ans[['title_x','overview','release_date']]
        ans = ans.rename(columns={'title_x' : 'original_title'})
        for index, row in ans.iterrows():
            st.write("==================================================================")
            st.write(index+1)
            st.write("Original Title:", row['original_title'])
            st.write("Release Date:", row['release_date'])
            st.write("Overview:", row['overview'])
            st.write("==================================================================")


if __name__ == "__main__":
    try:
        main = pd.read_csv('https://movie-buck.s3.ap-south-1.amazonaws.com/final_movies.csv')
        main['title']=main['title'].str.lower()
        main['original_title']=main['original_title'].str.lower()
        main.dropna(subset=['description'], inplace=True)
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(main['description'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        main = main.reset_index()
        titles = main['title']
        indices = pd.Series(main.index, index=main['title'])
        st.title("Content Model")
        st.title("Recommending similar movies")
        main['title']=main['title'].str.lower()
        main['original_title']=main['original_title'].str.lower()
        user_input= st.text_input("Enter movie")
        st.write("Recommending Movies: the big sleep,sabrina,the elephant man,shattered,miami vice")

        if user_input:
            recon = user_input
            st.title("Showing Results")
            result(recon)
        
    except Exception as e:
        st.error("An error occurred: " + str(e))
    








