from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Part 1 - Scraping rental property details (links, addresses, and prices)

# Set headers to mimic a real browser request to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Send a GET request to fetch the page content
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract property links
# Select anchor tags within the property card and extract their 'href' attributes
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a") 
all_links = [link["href"] for link in all_link_elements]
print(f"Found {len(all_links)} property links:\n", all_links)

# Extract property addresses
# Clean up addresses by removing newlines, pipe symbols, and extra whitespaces
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]
print(f"\nCleaned {len(all_addresses)} property addresses:\n", all_addresses)

# Extract property prices
# Select price spans and clean prices by removing "/mo" and any additional "+" info
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
print(f"\nCleaned {len(all_prices)} property prices:\n", all_prices)

# Part 2 - Filling in a Google Form using Selenium

# Configure Chrome to keep the browser open after the script finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Loop through all property details and fill out the Google Form
for n in range(len(all_links)):
    # Navigate to the Google Form (replace with your actual form link)
    driver.get("YOUR_GOOGLE_FORM_LINK_HERE")
    time.sleep(2)  # Wait for the page to load

    # Locate the input fields by their XPaths and fill them with the respective data
    address_input = driver.find_element(By.XPATH, 
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, 
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, 
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, 
                        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    # Fill out the form with the scraped address, price, and link
    address_input.send_keys(all_addresses[n])
    price_input.send_keys(all_prices[n])
    link_input.send_keys(all_links[n])
    
    # Submit the form
    submit_button.click()
