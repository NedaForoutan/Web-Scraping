## Required Libraries
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

# Base URL of the website Sportswear for the Women trainers product
base_url = "https://www.sportswear.de/en/women-trainers" # Name of the website has been anonymized.

# List of User-Agent strings to rotate through
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]

# Function to scrape a single page of products
def scrape_page(session, url):
    print(f"Scraping {url}")

    # Try to fetch the URL up to 5 times
    max_retries = 5
    for attempt in range(max_retries):
        try:
            headers = {
              "User-Agent": random.choice(user_agents),
              "Accept-Language": "en-US,en;q=0.9",
              "Referer": "https://www.sportswear.de/en/women-trainers",
              "Connection": "keep-alive",
            }
            response = session.get(url, headers=headers)
            response.raise_for_status()
            break  # Exit the loop if the request was successful
        except requests.exceptions.HTTPError as err:
            print(f"Attempt {attempt + 1} - Error fetching {url}: {err}")
            if attempt == max_retries - 1:  # If this was the last attempt
                print("Error fetching after multiple attempts. Exiting.")
                return []
            time.sleep(random.uniform(1, 3))  # Wait a bit before the next attempt

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract some product information
    products = []
    product_containers = soup.find_all('div', class_='glass-product-card__details')

    for product in product_containers:
        title = product.find('p', class_='glass-product-card__title').get_text(strip=True)
        category = product.find('p', class_='glass-product-card__category').get_text(strip=True)

        # Extracting the number of color variations
        color_variations_p = product.find('p', class_='glass-product-card__label')
        color_variations_span = color_variations_p.find('span', attrs={'data-auto-id': 'product-card-colvar-count'}) if color_variations_p else None
        color_variations = color_variations_span.get_text(strip=True) if color_variations_span else '1 colour'

        products.append({
            'title': title,
            'category': category,
            'color_variations': color_variations
        })

    return products

# Function to handle pagination and scrape all pages
def scrape_all_pages(start_url):
    all_products = []
    current_page = 1

    session = requests.Session()  # Use a session to persist cookies

    while True:
        # Calculate the start parameter based on the current page
        url = f"{start_url}?start={48 * (current_page - 1)}"
        products = scrape_page(session, url)

        if not products:
            break  # Stop if no products are found (likely the end of pagination)

        all_products.extend(products)
        current_page += 1

        # Random sleep to avoid getting blocked by the server
        time.sleep(random.uniform(3, 7))

    return all_products

# Function to save products to a CSV file
def save_to_csv(products, filename='sportswear_women_trainers.csv'):
    if not products:
        print("No products found to save.")
        return

    keys = products[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)

    print(f"Data saved to {filename}")

# Main execution
if __name__ == "__main__":
    start_url = base_url  # Start from the first page URL provided

    all_products = scrape_all_pages(start_url)

    if all_products:
        save_to_csv(all_products)
    else:
        print("No products were found.")

