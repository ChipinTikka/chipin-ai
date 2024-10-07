from flask import Flask, render_template, request
from flask_cors import CORS  # Import CORS
from vision import get_predictions

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        return render_template('index.html', predictions=None)
    elif request.method == 'POST' and request.files:
        file_image = request.files['image']
        if file_image:
            predictions = get_predictions(file_image)
            return render_template("index.html", predictions=predictions)
    return render_template('index.html', predictions=None)

if __name__ == "__main__":
    app.run(debug=True)
