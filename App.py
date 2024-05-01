import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
pipe = pipeline('summarization', model='t5-small')

# Create an option for summarizing text or URL content
summary_type = st.radio("Summarize from:", ["Text Input", "URL"])

# Depending on the selection, create appropriate input fields
if summary_type == "Text Input":
    input_text = st.text_area("Enter text to summarize:", height=150)

    # Button to trigger summarization
    if st.button("Summarize"):
        if input_text:
            # Summarize the text
            summary = pipe(input_text, max_length=100, clean_up_tokenization_spaces=True)[0]["summary_text"]
            st.write("Summary:")
            st.write(summary)
        else:
            st.write("Please enter some text to summarize.")

elif summary_type == "URL":
    url = st.text_input("Enter URL to summarize:")
    
    # Fetch and summarize from URL
    if st.button("Fetch and Summarize"):
        try:
            from newspaper import Article
            article = Article(url)
            article.download()
            article.parse()
            input_text = article.text

            # Now summarize
            summary = pipe(input_text, max_length=100, clean_up_tokenization_spaces=True)[0]["summary_text"]
            st.write("Summary:")
            st.write(summary)

        except Exception as e:
            st.write("Error fetching or summarizing the article. Try again with a valid URL
