from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
#def hello_world():
#    return "<p>Hello, World!</p>"

@app.route('/prompt',  methods=['POST'])
def prompt():
    resultat = {"answer": request.form["prompt"]}
    return resultat

@app.route('/question', methods=['GET'])
def 
