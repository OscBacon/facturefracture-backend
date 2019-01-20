import os
from flask import Flask, request, jsonify
import string
import random
import json
from imagescanner import scan_image

BILL_ATTRIBUTES = ['split-by', 'participants', 'unassigned', 'unpaid', 'paid', 'total', 'final']
UPDATE_TYPES = ['total', 'user-amount', 'paid', 'split-by', 'final', 'remove-user']

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
    with open(filepath, 'w') as f:
        json.dump(bill, f)

    json_filepath = "https://facturefracture.blob.core.windows.net/bills-json/" + code + '.json'
    return jsonify(message='User added!', json_filepath=json_filepath)


@app.route("/update_bill", methods=["POST"])
def update_bill():
    args = request.get_json()
    code = args.get("code")
    if not code or not os.path.isfile(_get_json_from_code(code)):
        return jsonify(message="invalid code"), 400

    update_type = args.get("update_type")
    if not update_type or update_type not in UPDATE_TYPES:
        return jsonify(message="invalid update type"), 400

    # Assume that if there is an update_type, appropriate key, value pairs are provided
    with open(_get_json_from_code(code), 'r') as f:
        bill = json.load(f)

    if update_type == "total":
        if bill['final']:
            return jsonify(message="can't edit finalized bill"), 403
        total = args.get("total")
        _update_total(bill, total)

    elif update_type == "user-amount":
        if bill['final']:
            return jsonify(message="can't edit finalized bill"), 403
        user = args.get("user")
        amount = args.get("amount")
        _update_user_amount(bill, user, amount)

    elif update_type == "paid":
        if not bill['final']:
            return jsonify(message="can't pay for unfinalized bill"), 403
        user = args.get("user")
        _update_paid(bill, user)

    elif update_type == "remove-user":
        if bill['final']:
            return jsonify(message="can't remove user from finalized bill"), 403
        user = args.get("user")
        _remove_user(bill, user)

    elif update_type == "split-by":
        if bill['final']:
            return jsonify(message="can't edit finalized bill"), 403
        split_by = args.get("split-by")
        bill['split-by'] = split_by

    elif update_type == "final":
        final = args.get("final")
        bill['final'] = final

    with open(_get_json_from_code(code), 'w') as f:
        json.dump(bill, f)

    return 'Bill updated!'


def _update_total(bill, new_total):
    # cast new_total to a float to avoid issues with arithmetics
    bill['total'] = float(new_total)
    if bill['split-by'] == "total-even":
        num_participants = len(bill['participants'])
        for participant in bill['participants']:
            bill['participants'][participant] = new_total / num_participants
    elif bill['split-by'] == "total-uneven":
        bill['unassigned'] += new_total - bill['total']


def _update_user_amount(bill, user, amount):
    if amount < bill['unpaid'][user]:
        # amount is less than participant's current amount, increase unassigned amount
        difference = amount - bill['unpaid'][user]
        bill['unassigned'] += difference
        bill['unpaid'][user] = amount
    elif amount > bill['unpaid'][user]:
        # amount is more than participant's current amount, redistribute leftover amount to other users
        num_participants = len(bill['participants'])
        for participant in bill['participants']:
            if participant != user:
                bill['unpaid'][participant] = (bill['total'] - amount) / (num_participants - 1)


def _update_paid(bill, user):
    bill['paid'][user] = bill['unpaid'][user]
    bill['paid'].remove(user)


def _remove_user(bill, user):
    user_amount = bill['unpaid'].pop(user)
    bill['participants'].remove(user)

    if bill['split-by'] == "total-even":
        num_participants = len(bill['participants'])
        for participant in bill['participants']:
            bill['unpaid'][participant] = bill['total'] / num_participants

    elif bill['split-by'] == "total-uneven":
        bill['unassigned'] += user_amount


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
    filename = code + '.json'
    filepath = os.path.join(os.sep, 'bills-json', filename)
    with open(filepath, 'w+') as f:
        json.dump(bill_dict, f)
    return "https://facturefracture.blob.core.windows.net/bills-json/" + filename


def _get_json_from_code(code):
    return os.path.join(os.sep, 'bills-json', code + '.json')
