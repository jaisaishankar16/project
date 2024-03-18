
# login and API

# from flask import Flask, render_template, request, redirect, session
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from flask_pymongo import PyMongo
# from werkzeug.utils import secure_filename
# import os
# import json
# import requests
# from pymongo import MongoClient
# global total_amount
# total_amount = 0

# app = Flask(__name__)
# app.secret_key = "your_secret_key"
# app.config['UPLOAD_FOLDER'] = "static/files"

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['login']
# users_collection = db['login_data']

# class UploadFileForm(FlaskForm):
#     file = FileField("File")
#     submit = SubmitField("Upload File")

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     username = session.get('username')
#     if not username:
#         return redirect('/login')
#     print(session)
#     global total_amount
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         file = form.file.data
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
#         url = 'https://ocr2.asprise.com/api/v1/receipt'
#         image = "static/files/" + file.filename
#         res = requests.post(url,
#                             data={
#                                 'api_key': 'TEST',
#                                 'recognizer': 'auto',
#                                 'ref_no': 'ocr_python_api'
#                             },
#                             files={
#                                 'file': open(image, 'rb')
#                             }
#                             )
#         with open("response.json", 'w') as f:
#             json.dump(json.loads(res.text), f)

#         with open("response.json", "r") as f:
#             data = json.load(f)
#         invoice_date = data['receipts'][0]['date']
#         invoice_receipt_no = data['receipts'][0]['receipt_no']
#         invoice_merchant_name = data['receipts'][0]['merchant_name']
#         invoice_merchant_tax_no = data['receipts'][0]['merchant_tax_reg_no']
#         invoice_merchant_address = data['receipts'][0]['merchant_address']
#         invoice_items = data['receipts'][0]['items']
#         invoice_total = data['receipts'][0]['total']
#         text = data['receipts'][0]['ocr_text']
        
    #     try:
    #         total_amount += invoice_total
    #         return render_template('result.html',
    #                                 image=image,
    #                                 invoice_date=invoice_date,
    #                                 invoice_receipt_no=invoice_receipt_no,
    #                                 invoice_merchant_name=invoice_merchant_name,
    #                                 invoice_merchant_tax_no=invoice_merchant_tax_no,
    #                                 invoice_merchant_address=invoice_merchant_address,
    #                                 invoice_items=invoice_items,
    #                                 invoice_total=invoice_total,
    #                                 total_amount=total_amount,
    #                                 username=username)  # Pass username to template
    #     except Exception as e:
    #         if not text:
    #             msg = "Uploaded Invoice is not valid."
    #             return render_template('except.html', image=image, msg=msg, username=username)  # Pass username to template
    #         else:
    #             return render_template('text.html', image=image, text=text, username=username)  # Pass username to template
    # return render_template('index.html', form=form, username=username)  # Pass username to template

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in session:
#         return redirect('/')
    
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = users_collection.find_one({'email': email, 'password': password})
#         if user:
#             session['username'] = user['username']  # Store username in session
#             return redirect('/')
#         else:
#             error = "Invalid username or password"
#             return render_template('login.html', error=error)
#     else:
#         return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if 'username' in session:
#         return redirect('/')
    
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         if users_collection.find_one({'email': email}):
#             error = "Username already exists"
#             return render_template('register.html', error=error)
#         users_collection.insert_one({'username': username, 'email': email, 'password': password})
#         session['username'] = username  # Store username in session
#         return redirect('/')
#     else:
#         return render_template('register.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     session.pop('total_amount', None)
#     return redirect('/login')

# if __name__ == '__main__':
#     app.run(debug=True)









# image to db



from flask import Flask, render_template, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
import json
import requests
from pymongo import MongoClient
from datetime import datetime



app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = "static/files"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['login']
users_collection = db['login_data']
images_collection = db['images']

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    if not username:
        return redirect('/login')
    
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename))
        url = 'http://ocr.asprise.com/api/v1/receipt'
        image_path = "static/files/" + filename
        res = requests.post(url,
                            data={
                                'api_key': 'TEST',
                                'recognizer': 'auto',
                                'ref_no': 'ocr_python_api'
                            },
                            files={
                                'file': open(image_path, 'rb')
                            }
                            )
        with open("response.json", 'w') as f:
            json.dump(json.loads(res.text), f)

        with open("response.json", "r") as f:
            data = json.load(f)

        # Extract relevant information from OCR response
        invoice_date = data['receipts'][0]['date']
        invoice_receipt_no = data['receipts'][0]['receipt_no']
        invoice_merchant_name = data['receipts'][0]['merchant_name']
        invoice_merchant_tax_no = data['receipts'][0]['merchant_tax_reg_no']
        invoice_merchant_address = data['receipts'][0]['merchant_address']
        invoice_items = data['receipts'][0]['items']
        invoice_total = data['receipts'][0]['total']
        text = data['receipts'][0]['ocr_text']

        # Store image data in MongoDB collection
        images_collection.insert_one({
            'username': username,
            'upload_date': datetime.now(),
            'filename': filename,
            'image_path': image_path,
            'total': invoice_total
        })

        try:
            return render_template('result.html',
                                    image=image_path,
                                    invoice_date=invoice_date,
                                    invoice_receipt_no=invoice_receipt_no,
                                    invoice_merchant_name=invoice_merchant_name,
                                    invoice_merchant_tax_no=invoice_merchant_tax_no,
                                    invoice_merchant_address=invoice_merchant_address,
                                    invoice_items=invoice_items,
                                    invoice_total=invoice_total,
                                    username=username)  # Pass username to template
        except Exception as e:
            if not text:
                msg = "Uploaded Invoice is not valid."
                return render_template('except.html', image=image_path, msg=msg, username=username)  # Pass username to template
            else:
                return render_template('text.html', image=image_path, text=text, username=username)  # Pass username to template
    return render_template('index.html', form=form, username=username)  # Pass username to template
    

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect('/login')
    
    # Retrieve all uploaded images by the current user
    user_images = images_collection.find({'username': username})
    print(user_images)
    return render_template('dashboard.html', user_images=user_images, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            session['username'] = user['username']  # Store username in session
            return redirect('/')
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if users_collection.find_one({'email': email}):
            error = "Username already exists"
            return render_template('register.html', error=error)
        users_collection.insert_one({'username': username, 'email': email, 'password': password})
        session['username'] = username  # Store username in session
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('total_amount', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)










