import os
from flask import Flask, flash, request, redirect, url_for, render_template, \
    send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import string
import random
from manage_blobs import upload_blob
import base64

UPLOAD_FOLDER = os.path.join('static','uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my dude'

# Currently, bills can be uploaded on a webpage
@app.route("/create_bill", methods=["GET", "POST"])
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
            timestamp = datetime.now().strftime('%d%m%y%H%M%S')
            filename = code + '_' + timestamp + '.jpg'

            try:
                filepath = os.path.join(os.sep, "/bills-images", filename)
                file.save(filepath)
                azure_filepath="https://facturefracture.blob.core.windows.net/bills-images/" + \
                    filename
                return render_template("uploaded_file.html",
                                       filepath=azure_filepath, code=code)

            except:
                flash("Upload Error!")
                return redirect(request.url)

    return render_template("upload_file.html")


def uploaded_file(filename):
    return os.path.join(UPLOAD_FOLDER, filename)

def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
                   for _ in range(6))

def create_json(code, total, user):
    dict = {
        'split-by': total,
        'participants':[user],
        'unassigned':0.00,
        'unpaid': {
            user: total
        },
        'paid': {},
        'total': total,
        'dinnerdaddy':user,
        'final': false
    }
