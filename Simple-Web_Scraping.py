
# Required Libraries
import requests
from bs4 import BeautifulSoup

# Get URL from the input
url = input("Enter the URL of the webpage you want to scrape: ")

# Send an HTTP request to the specified URL
try:
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Parse the content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Extract information:

# Extract all headings (h1, h2, etc.)
print("\nHeadings:")
headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
for heading in headings:
    print(heading.text.strip())

# Extract all paragraph text
print("\nParagraphs:")
paragraphs = soup.find_all('p')
for paragraph in paragraphs:
    print(paragraph.text.strip())

# Extract all links and linked pages (anchor tags)
print("\nLinked pages:")
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    text = link.text.strip()
    print(f"Link Text: {text} | URL: {href}")

