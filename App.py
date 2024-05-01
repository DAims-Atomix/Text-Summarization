import streamlit as st
from transformers import pipeline
from newspaper import Article

# Load the summarization pipeline
pipe = pipeline("summarization", model="t5-small")

# Create an option for the user to choose between text input and URL
summary_type = st.radio("Summarize from:", ["Text Input", "URL"])

# Depending on the selection, create appropriate input fields
if summary_type == "Text Input":
    input_text = st.text_area("Enter text to summarize:", height=150)
    if input_text and st.button("Summarize"):
        # Add TL;DR to indicate summary
        query = input_text + "\nTL;DR:\n"
        # Summarize the text
        try:
            pipe_out = pipe(query, max_length=100, clean_up_tokenization_spaces=True)
            summary = pipe_out[0]["summary_text"]
            st.write("Summary:")
            st.write(summary)
        except Exception as e:
            st.write("Error summarizing the text. Please try again.")

elif summary_type == "URL":
    url = st.text_input("Enter URL to summarize:")
    if st.button("Fetch and Summarize"):
        if url and url.startswith(("http://", "https://")):  # Check for valid URL format
            try:
                article = Article(url)
                article.download()
                article.parse()
                input_text = article.text
                # Now summarize
                query = input_text + "\nTL;DR:\n"
                pipe_out = pipe(query, max_length=100, clean_up_tokenization_spaces=True)
                summary = pipe_out[0]["summary_text"]
                st.write("Summary:")
                st.write(summary)
            except Exception as e:
                st.write("Error fetching or summarizing the article. It might be protected against scraping or is not valid. Please try another URL.")
        else:
            st.write("Please enter a valid URL (starting with http:// or https://).")
