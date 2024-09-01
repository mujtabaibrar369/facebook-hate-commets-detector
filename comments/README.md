# Facebook Comment Scraper and Hate Speech Analyzer

This project is a web application that scrapes comments from a specified Facebook post and analyzes them to determine if they contain hate speech. The application consists of a React frontend and a Flask backend, using Selenium to scrape Facebook comments and a pre-trained machine learning model to detect hate speech.

## Features

- **Scrape Comments:** Extracts comments and replies from a given Facebook post.
- **Hate Speech Detection:** Uses a pre-trained model to analyze comments for hate speech.
- **Interactive UI:** A React-based frontend for user interaction and result display.

## Prerequisites

- **Python 3.7+** and pip
- **Node.js** and npm
- **Google Chrome** installed for Selenium
- **Facebook Account:** A Facebook account is required to log in and scrape comments.

## Installation

### Backend (Flask)

1. Clone the repository:

   ```
   git clone https://github.com/mujtabaibrar369/facebook-hate-comments-detector.git
   ```

2. Create a virtual environment:

   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required Python packages:

   ```

   ```

5. Start the Flask server:
   ```
   flask run
   ```

### Frontend (React)

1. Navigate to the frontend directory:

   ```
   cd ../frontend
   ```

2. Install the required npm packages:

   ```
   npm install
   ```

3. Start the React development server:

   ```
   npm start
   ```

4. Open your web browser and visit `http://localhost:3000` to access the application.
