import os
from flask import Flask, flash, request, redirect, render_template, jsonify
import string
import random
import json
from imagescanner import scan_image


app = Flask(__name__)
app.secret_key = 'my dude'


@app.route("/create_bill", methods=["POST"])
def create_bill():
    if 'user' not in request.form or request.form['user'] == '':
        return jsonify(message="no user given"), 400
    if 'photo' not in request.files:
        return jsonify(message="no file uploaded"), 400
    file = request.files['photo']
    user = request.form['user']

    code = generate_code()
    filename = code + '.jpg'

    filepath = os.path.join(os.sep, "bills-images", filename)
    file.save(filepath)
    image_filepath = "https://facturefracture.blob.core.windows.net/bills-images/" + filename
    total = scan_image(image_filepath)
    if total == -1:
        return jsonify(message="bill not recognized"), 502
    json_filepath = create_json(code, total, user)

    return jsonify(code=code, json_filepath=json_filepath)


def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def create_json(code, total, user):
    bill_dict = {
        'split-by': 'total-even',
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