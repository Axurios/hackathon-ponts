from flask import Flask, render_template, request
# from ask_question_to_pdf import gpt3_completion, add_new_message
from ask_question_to_pdf import initialize_memory, ask_question_pdf
Historic = initialize_memory()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

# def hello_world():
#    return "<p>Hello, World!</p>"


@app.route('/prompt',  methods=['POST'])
def prompt():
    return {"answer": ask_question_pdf(histo=Historic,
                                       user_message=request.form["prompt"])}
    # conversation = add_new_message(memory=Historic,
    # new=request.form["prompt"])
    # return {"answer": gpt3_completion(conversation)}


# def prompt():
    # conversation = add_new_message(memory=Historic,
    # new=request.form["prompt"])
    # return {"answer": gpt3_completion(conversation)}
    # without the pdf as ground truth

# @app.route('/question',  methods=['GET'])
# def ask():
