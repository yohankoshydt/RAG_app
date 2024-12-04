import pandas as pd

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

def get_content_text(url):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

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