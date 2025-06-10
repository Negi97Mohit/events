# Eventbrite Event ID Scraper using Requests and BeautifulSoup
#
# Description:
# This script automates the process of visiting the Eventbrite website for all events in Ireland,
# navigating through all available pages by making direct HTTP requests,
# and scraping the unique event ID for each event from the HTML.
# The collected IDs are then saved into a CSV file.
#
# What you need to run this script:
# 1. Python 3.x installed on your computer.
# 2. The 'requests' and 'beautifulsoup4' libraries. If you don't have them, open your
#    terminal or command prompt and run:
#    pip install requests beautifulsoup4

import csv
import time
import requests
from bs4 import BeautifulSoup

def scrape_eventbrite_event_ids():
    """
    Scrapes all event IDs from Eventbrite's Ireland events pages using
    requests and BeautifulSoup and saves them to a CSV file.
    """
    # --- Configuration ---
    # Base URL for the event search. The page number will be formatted into it.
    base_url = "https://www.eventbrite.ie/d/ireland/all-events/?page={}"
    
    # Headers to mimic a browser visit, which can help avoid getting blocked.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Scraper initialized.")
    
    all_event_ids = set() # Use a set to automatically handle duplicates
    page_num = 1

    # --- Loop through all pages until no more events are found ---
    while True:
        current_url = base_url.format(page_num)
        print(f"\nScraping page {page_num}...")
        print(f"URL: {current_url}")
        
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all elements (specifically 'a' tags) with the 'data-event-id' attribute
            event_elements = soup.find_all('a', attrs={'data-event-id': True})
            
            # If no event elements are found, we've reached the last page
            if not event_elements:
                print(f"No more events found. Reached the end at page {page_num - 1}.")
                break

            page_ids = set()
            for element in event_elements:
                event_id = element.get('data-event-id')
                if event_id and event_id.isdigit():
                    page_ids.add(event_id)
            
            if page_ids:
                print(f"Found {len(page_ids)} unique event IDs on this page.")
                all_event_ids.update(page_ids)
            else:
                # If there are event elements but no valid IDs, something is wrong
                print(f"No valid event IDs found on page {page_num}, stopping.")
                break
            
            # Increment the page number for the next iteration
            page_num += 1
            
            # A respectful delay to avoid overwhelming the server
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page_num}. Error: {e}. Stopping.")
            break
        except Exception as e:
            print(f"An error occurred on page {page_num}: {e}")
            break

    # --- Step 3: Save the results to a CSV file ---
    if all_event_ids:
        output_file = 'eventbrite_event_ids_requests.csv'
        print(f"\nScraping complete. Found a total of {len(all_event_ids)} unique event IDs.")
        print(f"Saving results to {output_file}...")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Event ID']) # Write header
                for event_id in sorted(list(all_event_ids)): # Sort for consistent output
                    writer.writerow([event_id])
            print(f"Successfully saved event IDs to {output_file}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print("No event IDs were scraped.")

    print("\nScript finished.")

# --- Run the scraper ---
if __name__ == "__main__":
    scrape_eventbrite_event_ids()
