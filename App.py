import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
pipe = pipeline('summarization', model='t5-small')

# Create a text input for users to enter text
#input_text = st.text_area("Enter text to summarize:", height=150)

if summary_type == "Text Input":
    input_text = st.text_area("Enter text to summarize:", height=150)
elif summary_type == "URL":
    url = st.text_input("Enter URL to summarize:")
    if st.button("Fetch and Summarize"):
        try:
            # Fetch the article from the URL
            article = Article(url)
            article.download()
            article.parse()
            input_text = article.text
        except Exception as e:
            st.write("Error fetching the article. Please ensure the URL is valid.")
            input_text = None

# Button to trigger summarization
if st.button("Summarize"):
    if input_text:
        # Add TL;DR to indicate summary
        query = input_text + "\nTL;DR:\n"
        # Summarize the text
        pipe_out = pipe(query, max_length=512, clean_up_tokenization_spaces=True)
        # Display the summarized text
        summary = pipe_out[0]['summary_text']
        st.write("Summary:")
        st.write(summary)
    else:
        st.write("Please enter some text to summarize.")
