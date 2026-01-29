# GitHub Webhook Activity Monitor

This project shows live GitHub repository activity using webhooks.

Whenever a **push**, **pull request**, or **merge** happens on a GitHub repository, the event is sent to a Flask server, stored in MongoDB, and displayed on a web page that updates automatically every 15 seconds.

---

## Features

- Receives GitHub webhook events  
- Stores events in MongoDB  
- Displays recent activity on a clean UI  
- Auto-refreshes every 15 seconds  

---

## Tech Stack

- Python (Flask)
- MongoDB
- HTML, CSS, JavaScript
- GitHub Webhooks
- Ngrok (for local testing)

---

## How to Run Locally

1. Clone the repository  
2. Create and activate a virtual environment  
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
# GitHub Webhook Activity Monitor

This project shows live GitHub repository activity using webhooks.

Whenever a **push**, **pull request**, or **merge** happens on a GitHub repository, the event is sent to a Flask server, stored in MongoDB, and displayed on a web page that updates automatically every 15 seconds.

---

## Features

- Receives GitHub webhook events  
- Stores events in MongoDB  
- Displays recent activity on a clean UI  
- Auto-refreshes every 15 seconds  

---

## Tech Stack

- Python (Flask)
- MongoDB
- HTML, CSS, JavaScript
- GitHub Webhooks
- Ngrok (for local testing)

---

## How to Run Locally

1. Clone the repository  
2. Create and activate a virtual environment  
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
4. Start MongoDB

5. Run the Flask app
    python app.py

6. Open in browser
    http://localhost:5000