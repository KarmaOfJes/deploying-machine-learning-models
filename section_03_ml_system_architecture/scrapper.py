import requests
from bs4 import BeautifulSoup
import pdfkit
import re
import os

# Base URL of the book
base_url = 'https://sre.google/sre-book/'

# Headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Get the table of contents page
toc_url = f'{base_url}table-of-contents/'
response = requests.get(toc_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all chapter links from the Table of Contents
chapter_links = soup.find_all('a', href=True)


# Function to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


# Iterate through each chapter link
for link in chapter_links:
    chapter_name = link.text.strip()
    chapter_url = link['href']

    # Only process valid chapter URLs
    if chapter_url.startswith('/sre-book/'):
        full_url = f'https://sre.google{chapter_url}'

        # Fetch chapter content
        chapter_response = requests.get(full_url, headers=headers)
        chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')

        # Extract content, assuming it's in <article> tags
        chapter_content = chapter_soup.find('article')

        if chapter_content:
            # Convert content to HTML string
            html_content = str(chapter_content)

            # Generate the PDF filename based on the chapter name
            sanitized_name = sanitize_filename(chapter_name)
            pdf_filename = f'google_se_architecture/{sanitized_name}.pdf'

            # Save HTML content as PDF
            pdfkit.from_string(html_content, pdf_filename)
            print(f'Saved {pdf_filename}')