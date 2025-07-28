import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL (page number will be inserted using .format)
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# Create and open CSV file to store product data
file = open("products.csv", mode="w", newline="", encoding="utf-8")
writer = csv.writer(file)

# Write header row in CSV
writer.writerow(["Product Name", "Price", "Rating"])

# Loop through the first 5 pages (you can increase the number)
for page_number in range(1, 6):
    url = BASE_URL.format(page_number)
    print(f"Scraping page {page_number}...")

    response = requests.get(url)

    # Check if page loaded successfully
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all("article", class_="product_pod")

        for product in products:
            # Extract product name
            name = product.h3.a["title"]

            # Extract price
            price = product.find("p", class_="price_color").text.strip()

            # Extract rating from class (e.g., "Three", "Five")
            rating = product.p["class"][1]

            # Write to CSV
            writer.writerow([name, price, rating])

            # Print to console
            print(f"Scraped: {name} | {price} | {rating}")
    else:
        print(f"Failed to load page {page_number}")

    # Delay between requests to be polite
    time.sleep(1)

# Close the CSV file
file.close()
print("\n✅ Done! Data saved to 'products.csv'")
