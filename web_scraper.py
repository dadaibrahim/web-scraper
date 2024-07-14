import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape quotes from a website
def scrape_quotes(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data from {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_data = []

    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({'text': text, 'author': author, 'tags': tags})

    return quotes_data

# Streamlit App
st.title("Interactive Web Scraping")

url = st.text_input("Enter the URL of the website to scrape", "http://quotes.toscrape.com/")
if st.button("Scrape"):
    quotes = scrape_quotes(url)
    if quotes:
        st.success(f"Found {len(quotes)} quotes")
        for quote in quotes:
            st.write(f"**Quote:** {quote['text']}")
            st.write(f"_Author:_ {quote['author']}")
            st.write(f"Tags: {', '.join(quote['tags'])}")
            st.write("---")
    else:
        st.warning("No quotes found or unable to scrape the website.")
