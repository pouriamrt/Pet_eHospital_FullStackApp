from app.main import bp
from flask import render_template, request
from flask_login import login_required, current_user
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@bp.route('/')
@login_required
def index():
    global messages
    messages=[
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital app that gives a short general solution."},
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital app that recommends a suitable online hospital department webpage in my app to the customer."},
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital which its departments are general, dental, orthopedic and surgery."}
    ]
    return render_template('index.html', name=current_user.name)

@bp.route("/get", methods=["POST"])
@login_required
def chat():
    msg = request.form["msg"]
    return get_Chat_response(msg)

def get_Chat_response(text):
    if text:
        messages.append({"role": "user", "content": text})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.5
        )

        reply = completion.choices[0].message.content
        messages.extend([{"role": "assistant", "content": text}, {"role": "assistant", "content": reply}])
        # print(messages)
        return reply
