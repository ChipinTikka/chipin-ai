from flask import Flask, render_template, request
from flask_cors import CORS
from vision import get_predictions
import requests
import json

app = Flask(__name__)
CORS(app)

ollama_url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        return render_template('index.html', predictions=None)
    elif request.method == 'POST' and request.files:
        file_image = request.files['image']
        if file_image:
            predictions = get_predictions(file_image)
            data = {
                "model": "llama3.2",
                "prompt": "I am providing you with a json containing receipt OCR data, format it properly into item price quantity. add tax as an item as well: "+ str(predictions),
                "format": "json",
                "stream": False
            }

            # Send request to Ollama API
            response = requests.post(ollama_url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                result = response.json()
                predictions = result.get("response", "No response from Ollama model")
            else:
                predictions = f"Error: {response.status_code} - {response.text}"

            return render_template("index.html", predictions=predictions)
    return render_template('index.html', predictions=None)

if __name__ == "__main__":
    app.run(debug=True, port=8009)
