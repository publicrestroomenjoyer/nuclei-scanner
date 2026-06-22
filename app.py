import os
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form.get("target")
    if not target:
        return "Please provide a target URL", 400

    # Ensure directory exists
    os.makedirs("results", exist_ok=True)

    cmd = ["nuclei", "-u", target, "-json-export", "results/output.json"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return "Scan completed successfully!"
    except subprocess.CalledProcessError as e:
        return f"Scan failed. Error: {e.stderr}", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
