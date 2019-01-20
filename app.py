import os
from flask import Flask, flash, request, redirect, render_template, jsonify
import string
import random
import json

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my dude'


@app.route("/create_bill", methods=["POST"])
def create_bill():
    if request.method == "POST":
        if 'photo' not in request.files:
            flash("No file uploaded!")
            print("no file uploaded")
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)

        if file:
            code = generate_code()
            filename = code + '.jpg'

            filepath = os.path.join(os.sep, "bills-images", filename)
            file.save(filepath)
            azure_filepath = "https://facturefracture.blob.core.windows.net/bills-images/" + \
                filename
            return jsonify(code=code)


def uploaded_file(filename):
    return os.path.join(UPLOAD_FOLDER, filename)


def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def create_json(code, total, user):
    bill_dict = {
        'split-by': total,
        'participants': [user],
        'unassigned': 0.00,
        'unpaid': {
            user: total
        },
        'paid': {},
        'total': total,
        'dinnerdaddy': user,
        'final': False
    }
    json_bill = json.dumps(bill_dict)
    filename = code + '.json'
    filepath = os.path.join(os.sep, 'bills-json', filename)
    with open(filepath, 'w+') as f:
        f.write(json_bill)
