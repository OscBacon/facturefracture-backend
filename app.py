import os
from flask import Flask, flash, request, redirect, url_for, render_template, \
    send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import string
import random
from manage_blobs import upload_blob

UPLOAD_FOLDER = os.path.join('static','uploads')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if file has an allowed extension
def allowed_extension(extension):
    return extension in ALLOWED_EXTENSIONS

# Currently, bills can be uploaded on a webpage
@app.route("/create_bill", methods=["GET", "POST"])
def create_bill():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file uploaded!")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)

        extension = file.filename.rsplit('.', 1)[1].lower()

        if file and '.' in file.filename and allowed_extension(extension):
            code = generate_code()
            timestamp = datetime.now().strftime('%d%m%y%H%M%S')
            filename = code + '_' + timestamp + '.' + extension

            try:
                file.save(os.path.join("bills-images", filename))
                # upload_blob(filename, uploaded_file(filename))
                # filepath="https://facturefracture.blob.core.windows.net/bills-images/" + \
                    # filename
                filepath = os.path.join("bills-images", filename)
                # os.remove(url_for('uploaded_file', filename=filename))
                return render_template("uploaded_file.html",
                                       filepath=filepath, code=code)

            except:
                flash("Upload Error!")
                return redirect(request.url)

    return render_template("upload_file.html")


def uploaded_file(filename):
    return os.path.join(UPLOAD_FOLDER, filename)

def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
                   for _ in range(6))
