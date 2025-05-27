from flask import Flask
from threading import Thread

# Flask app for keeping the repl alive
app = Flask('')

# Route for the home page
@app.route('/')
# Function to return a simple message
def home():
    return "I'm alive"
    # Run the app on port 8080
def run():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

# Function to keep the repl alive
def keep_alive():
    t = Thread(target=run)
    t.start()
  