# Filename: web_scraper.py

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Function to scrape data from a webpage
def scrape_article_titles(url):
    # Step 1: Make HTTP request
    response = requests.get(url)

    # Check for a successful response
    if response.status_code != 200:
        print(f"Error fetching the page: {response.status_code}")
        return []

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Extract data for each column
    titles = [title.get_text(strip=True) for title in soup.find_all('div', class_='pollster-name')]
    sample = [samp.get_text(strip=True) for samp in soup.find_all('td', class_='sample')]
    sample_type = [stype.get_text(strip=True) for stype in soup.find_all('td', class_='sample-type')]
    date = [d.get_text(strip=True) for d in soup.find_all('div', class_='date-wrapper')]

    # Step 4: Extract 'net' values and determine party affiliation
    party = []
    net_values = []
    for net in soup.find_all('td', class_='net'):
        net_values.append(net.get_text(strip=True))  # Get the actual text content for 'Net'
        classes = net.get("class", [])
        if 'dem' in classes:
            party.append("Democrat")
        elif 'rep' in classes:
            party.append("Republican")
        else:
            party.append("Independent")  # Default if no specific class is present

    # Combine data into a list of dictionaries for each entry
    data = [
        {"Title": t, "Sample": s, "Sample Type": st, "Date": d, "Party": p, "Net": n} 
        for t, s, st, d, p, n in zip(titles, sample, sample_type, date, party, net_values)
    ]

    return data

# Step 5: Store results in CSV format with multiple columns
def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    # Define the column headers based on the dictionary keys
    fieldnames = ["Title", "Sample", "Sample Type", "Date", "Party", "Net"]

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write each dictionary as a row

# Main function to run scraper
if __name__ == '__main__':
    url = 'https://projects.fivethirtyeight.com/polls/president-general/2024/national/'  # Replace with your target URL
    data = scrape_article_titles(url)
    if data:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"polls_snapshot_{current_time}.csv"
        save_to_csv(data, filename)
        print(f"Data saved to {filename}")
    else:
        print("No titles found or error fetching data.")




#START VISUALIZATIONS
#
##
###
####
#####
#   polls_snapshot_2024-10-26_23-21-13.csv
import pandas as pd
import plotly.express as px

# Load your data
filename = "polls_snapshot_2024-10-26_23-21-13.csv"  # Replace with actual filename
data = pd.read_csv(filename)

# Convert 'Date' column to a datetime object if required
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Example: Inline bar chart for party distribution
fig = px.bar(data, x='Party', title="Distribution of Party Affiliation")

# Save as HTML
fig.write_html("party_distribution.html")  # Saves the interactive chart as an HTML file
