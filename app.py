import os
import subprocess
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form.get("target")
    if not target:
        return jsonify({"error": "Please provide a target URL"}), 400

    # Ensure directory exists
    os.makedirs("results", exist_ok=True)
    output_path = "results/output.json"
    
    # Run nuclei with json-export
    cmd = ["nuclei", "-u", target, "-json-export", output_path]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Read the generated JSON file
        results = []
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                for line in f:
                    results.append(json.loads(line))
        
        # Return the actual scan data
        return jsonify({"status": "success", "results": results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
