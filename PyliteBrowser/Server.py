from flask import Flask,render_template
from flask_cors import CORS
app = Flask(__name__,template_folder="View",static_folder='Assets')
CORS(app)

@app.route('/api/data')
def get_data():
    return {"message": "Hello from Flask!"}

@app.route("/")
def index():
    return render_template("Main.html")


if __name__ == '__main__':
    app.run(debug=True)
