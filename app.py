import os
from flask import Flask, flash, request, redirect, render_template, jsonify
import string
import random
import json
from imagescanner import scan_image

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my dude'


@app.route("/create_bill", methods=["POST"])
def create_bill():
    if request.method == "POST":
        if 'user' not in request.form:
            print("no user given")
            return redirect(request.url)
        if 'photo' not in request.files:
            print("no file uploaded")
            return redirect(request.url)
        file = request.files['photo']
        user = request.form['user']
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)

        if file and user:
            code = generate_code()
            filename = code + '.jpg'

            filepath = os.path.join(os.sep, "bills-images", filename)
            file.save(filepath)
            image_filepath = "https://facturefracture.blob.core.windows.net/bills-images/" + filename
            total = scan_image(image_filepath)
            json_filepath = create_json(code, total, user)

            return jsonify(code=code, json_filepath=json_filepath)


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
    return "https://facturefracture.blob.core.windows.net/bills-json/" + filename
