#This file downloads the HTML of a page automatically.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.common.by import By

# Canvas login URL
login_url = 'https://canvas.oregonstate.edu/'

# Canvas username and password
username = "chattera"
password = "breatheagain444"

# Start a Chrome driver and navigate to the login page
driver = webdriver.Chrome()
driver.get(login_url)

# Find the username and password fields and submit button
username_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')
submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

# Enter the login credentials and submit the form
username_field.send_keys(username)
password_field.send_keys(password)
submit_button.click()

# Wait for the page to load after login
time.sleep(20)

# URLs of the Canvas pages you want to access
urls = ['https://canvas.oregonstate.edu/courses/1870084', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792467', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792468', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8880307', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792470', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792450', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8863789', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8863816', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792449', 'https://canvas.oregonstate.edu/courses/1870084/assignments/8792464']

# Navigate to the Canvas page
i=3
for url in urls:
	driver.get(url)

# Get the HTML source code of the page
	html = driver.page_source
	filename = f"CanvasHTMLoutput{i+1}"
	print(filename)

	with open(os.path.join(os.path.expanduser("~"), "Downloads", f"{filename}.html"), "w") as f:
		f.write(html)

	i=i+1

print("done")

# Close the driver
driver.quit()
