# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:51:48 2023

@author: shwet
"""

import streamlit as st
from PIL import Image

if __name__ == '__main__':
    try:

        st.write("==================================================================")
        st.title("   Movies Recommendation   ")
        st.write("==================================================================")
      
        # Load the image using PIL
        image_path = "/recommender_App/img2.jpeg"  # Replace with the actual image file path
        image = Image.open(image_path)
        

        # Display the image using st.image with increased width
        st.image(image, caption="MOVIE DISPLAY", width=1000)
        st.markdown("[Click here to see Data Analysis](https://public.tableau.com/app/profile/ritesh.kushwaha7191/viz/MovieRecommendationSystem_16931382236530/Story1?publish=yes)")
      
     
    except Exception as e:
        st.error("An error occurred: " + str(e))
