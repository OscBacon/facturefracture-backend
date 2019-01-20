import os
from flask import Flask, request, jsonify
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
        delete_bill(code)
        return jsonify(message="bill not recognized"), 502
    json_filepath = create_json(code, total, user)

    return jsonify(code=code, json_filepath=json_filepath)

@app.route("/add_participant", methods=["POST"])
def add_user():
    args = request.get_json()
    code = args.get("code")
    user = args.get("user")
    if not code or not user:
        return jsonify(message="missing argument"), 400

    filepath = os.path.join(os.sep, 'bills-json', os.sep, code + '.json')
    if not os.path.isfile(filepath):
        return jsonify(message="verification code is invalid"), 400

    with open(filepath, 'r') as f:
        bill = json.load(f)
    bill['participants'] += user
    bill['unpaid'][user] = 0.0
    if bill['split-by'] == 'total-even':
        num_participants = len(bill['participants'])
        for participant in bill['unpaid']:
            bill['unpaid'][participant] = bill['total'] / num_participants
    json_bill = json.dumps(bill)
    with open(filepath, 'w') as f:
        f.write(json_bill)
    return 'User added!'


def delete_bill(code):
    img_path = os.path.join(os.sep, 'bills-images', code + '.jpg')
    if os.path.isfile(img_path):
        os.remove(img_path)
    json_path = _get_json_from_code(code)
    if os.path.isfile(json_path):
        os.remove(json_path)


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

def _get_json_from_code(code):
    return os.path.join(os.sep, 'bills-json', code + '.json')