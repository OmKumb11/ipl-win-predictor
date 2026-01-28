import streamlit as st 
import pickle
import pandas as pd 

pip = pickle.load(open('pipe.pkl', 'rb'))

st.title("IPL Win Probability Predictor")

if st.button("Test the Brain"):
    st.write("This Mode is Loaded and Ready")