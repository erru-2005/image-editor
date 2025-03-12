from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"Processing {filename} with operation: {operation}")
    img = cv2.imread(f"uploads/{filename}")
    newFilename = f"static/{filename}"
    
    match operation:
        case "cgray":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
        case "blur":
            img = cv2.GaussianBlur(img, (15, 15), 0)
        case "canny":
            img = cv2.Canny(img, 100, 200)
        case "sharpen":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img = cv2.filter2D(img, -1, kernel)
        case "sepia":
            kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
            img = cv2.transform(img, kernel)
        case "cartoon":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            smooth = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 250, 250)
            img = cv2.bitwise_and(color, color, mask=edges)
        case "invert":
            img = cv2.bitwise_not(img)
    
    cv2.imwrite(newFilename, img)
    return newFilename

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/how")
def how_to_use():
    return render_template("how.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")
port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
app.run(debug=True, host="0.0.0.0", port=port)
