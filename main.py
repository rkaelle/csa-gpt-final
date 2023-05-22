import openai
import os

openai.api_key = os.environ['apikey']

import requests
from bs4 import BeautifulSoup

def scrape_wikipedia_content(url, max_tokens=4000):
    # Make a GET request to the Wikipedia page
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content element
    content = soup.find('div', {'class': 'mw-parser-output'})
    
    # Extract the text from the content element
    text = content.get_text()
    
    # Truncate the text to the desired number of tokens
    truncated_text = text[:max_tokens]
    
    return truncated_text


def save_to_file(text, file_path):
    with open(file_path, 'w') as file:
        file.write(text)

# Provide the Wikipedia page URL
wikipedia_url = input("insert wikepedia link here: ")

# Scrape the content from the Wikipedia page
content = scrape_wikipedia_content(wikipedia_url)

# Save the content to the chunk.txt file
save_to_file(content, 'chunk.txt')

print("Content scraped and saved to chunk.txt")


def summarize_text_file(file_path, max_tokens=600):
    with open(file_path, "r") as file:
        text = file.read()

    prompt = "Make organized cornell notes on the following text:\n\n" + text

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary


file_path = "chunk.txt"  
summary = summarize_text_file(file_path)
print("Summary:")
print(summary)
