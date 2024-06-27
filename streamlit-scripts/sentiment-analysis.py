from transformers import pipeline
import streamlit as st

#Load model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")


st.title("Sentiment Analysis")
user_input = st.text_input("Enter your message:")

if user_input:
# Perform sentiment analysis
    sentiment = sentiment_analyzer(user_input)[0]
    sentiment_label = sentiment["label"]
    sentiment_score = sentiment["score"]

    # Display bot response based on sentiment
    if sentiment_label == "POSITIVE":
        st.success("That sounds great! 😄  \n" +"Score: " + str(sentiment_score))
    else:
        st.error("I'm sorry to hear that. 😔  \n" +"Score: " + str(sentiment_score))




