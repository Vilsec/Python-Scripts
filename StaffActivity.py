# Script to monitor online presence of key team members in the Garden Elysium Server - Staff Activity Channel.
# It periodically checks for specified usernames and writes their online status to a text file.

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

# Configure Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")  # Disable notifications for less load
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL for Discord login page
login_url = "https://discord.com/login"
driver.get(login_url)

# Wait for manual login
input("Please log in to Discord and press Enter to continue...")

# URL of the channel to monitor
channel_url = 'https://discord.com/channels/1187388943776362637/1257895754140352562'
driver.get(channel_url)

# List of usernames to track for online status
TEAM_MEMBERS = ['kailyx', 'misthios', 'sadilus', 'caitriona']

while True:
    try:
        # Refresh element references each loop to avoid stale elements
        spans = driver.find_elements(By.TAG_NAME, "span")
        
        # Combine text content from spans for searching
        page_text = " ".join([el.text for el in spans if el.text.strip() != ""])
        
        # Check for presence of any usernames in the text
        online_members = [user for user in TEAM_MEMBERS if user.lower() in page_text.lower()]
        
        if online_members:
            print(f"Detected online team members: {', '.join(online_members)}. Writing 'Team Online' to file.")
            with open(r'C:\Users\dem\downloads\TeamStatus.txt', 'w', encoding='utf-8') as file:
                file.write("Team Online\n")
            print("Status updated to Team Online.")
        else:
            print("No team members detected online. Writing 'Team Offline' to file.")
            with open(r'C:\Users\dem\downloads\TeamStatus.txt', 'w', encoding='utf-8') as file:
                file.write("Team Offline\n")
            print("Status updated to Team Offline.")
        
        time.sleep(5)  # Wait 5 seconds before next check
    
    except StaleElementReferenceException:
        print("Detected stale elements, refreshing...")
        time.sleep(5)
        continue
    
    except Exception as error:
        print(f"An error occurred: {error}")
        break
