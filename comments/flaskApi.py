from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import joblib
import re

app = Flask(__name__)
CORS(app)

# Load the pre-trained hate speech detection model
model = joblib.load('hate_speech_model.pkl')

# Function to predict if a comment is hate speech
def is_hate_speech(comment):
    prediction = model.predict([comment])
    return bool(prediction[0])

# Function to scrape comments from a Facebook post
def scrape_facebook_comments(url, username, password):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.facebook.com/")
    time.sleep(2)

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(username)

    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.get(url)
    time.sleep(5)

    # Look for "All comments" option and click it
    try:
        all_comments_option = driver.find_element(By.XPATH, "//span[contains(text(), 'Most relevant')]")
        all_comments_option.click()
        time.sleep(2)

        all_comments_button = driver.find_element(By.XPATH, "//span[contains(text(), 'All comments')]")
        all_comments_button.click()
        time.sleep(5)
    except Exception as e:
        print("Error clicking 'All comments': ", e)

    # Click on "View all X replies" to expand all replies
    try:
        while True:
            view_more_replies = driver.find_elements(By.XPATH, "//div[@role='button' and contains(., 'View all')]")
            if not view_more_replies:
                break
            for reply_button in view_more_replies:
                try:
                    driver.execute_script("arguments[0].click();", reply_button)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error clicking 'View all replies': {e}")
    except Exception as e:
        print(f"Error handling 'View all replies': {e}")

    # Scroll and scrape comments
    Name = []
    Comment = []
    scroll_pause_time = 2
    max_attempts = 5
    attempts = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        comment_blocks = driver.find_elements(By.CLASS_NAME, "xmjcpbm.x1tlxs6b.x1g8br2z.x1gn5b1j.x230xth.x9f619.xzsf02u.x1rg5ohu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x193iq5w.x1mzt3pk.x1n2onr6.xeaf4i8.x13faqbe")

        for block in comment_blocks:
            try:
                name = block.find_element(By.CLASS_NAME, "xt0psk2").text
                comment = block.find_element(By.CLASS_NAME, "x1lliihq.xjkvuk6.x1iorvi4").text
                if name not in Name:
                    Name.append(name)
                    Comment.append(comment)
            except Exception as e:
                print(f"Error extracting data: {e}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Check if the page height has not changed (meaning no new comments loaded)
        if new_height == last_height:
            attempts += 1
            if attempts >= max_attempts:
                print("No more comments to load.")
                break
        else:
            attempts = 0  # Reset attempts if new comments are loaded
        
        last_height = new_height

    driver.quit()

    return [{"name": name, "comment": comment} for name, comment in zip(Name, Comment)]

@app.route('/analyze_comments', methods=['POST'])
def analyze_comments():
    data = request.json
    url = data['url']
    username = data['username']
    password = data['password']

    comments = scrape_facebook_comments(url, username, password)

    hate_comments = []
    non_hate_comments = []

    for comment in comments:
        if is_hate_speech(comment['comment']):
            hate_comments.append(comment)
        else:
            non_hate_comments.append(comment)

    hate_percentage = len(hate_comments) / len(comments) * 100 if comments else 0

    return jsonify({
        "total_comments": len(comments),
        "hate_comments": len(hate_comments),
        "non_hate_comments": len(non_hate_comments),
        "hate_percentage": hate_percentage,
        "comments": comments
    })

if __name__ == '__main__':
    app.run(debug=True)
