import pandas as pd
import streamlit as st

# Load the Excel file and specify the range of cells you want to load
  # Replace with your file path

def read_file(path):
    # Specify the range, e.g., rows 2 to 100 and columns A to D in 'Sheet1'
    df = pd.read_csv(path)
    df['Dashboard Title'] = df['Dashboard Title'].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else str(x)
)

    df = df.where(pd.notnull(df), None)

    return df


import requests
from bs4 import BeautifulSoup

def fetch_website(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)

        # Check the HTTP status code
        status_code = response.status_code
        if status_code == 200:
            st.success(f"Website info fetched successfully! Status code: {status_code}")
            return response  
        else:
            st.error(f"Failed to fetch the website. Status code: {status_code}")
            return None

    except requests.exceptions.MissingSchema:
        st.error("Invalid URL format. Please include 'http://' or 'https://'.")
        return None
    except requests.exceptions.InvalidURL:
        st.error("The URL provided is invalid. Please check and try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the URL. Please check your internet connection or the URL.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An unexpected error occurred: {e}")
        return None




def get_content_text(url):
    # Fetch the webpage content
    response = fetch_website(url)
    if response:
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements to avoid unnecessary text
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Extract text from the remaining elements
        text = soup.get_text(separator="\n", strip=True)

        # Clean up the text by removing extra blank lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content_text = "\n".join(lines)

        return content_text