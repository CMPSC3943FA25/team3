from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running!"

if __name__ == "__main__":
    print("Launching test server...")
    app.run(debug=True)
