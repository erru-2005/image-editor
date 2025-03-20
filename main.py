from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np
from werkzeug.exceptions import RequestEntityTooLarge

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    try:
        print(f"Processing {filename} with operation: {operation}")
        img = cv2.imread(f"uploads/{filename}")
        if img is None:
            raise ValueError("Failed to read the image file")
            
        newFilename = f"static/{filename}"
        
        if operation == "cgray":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif operation == "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
        elif operation == "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
        elif operation == "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
        elif operation == "blur":
            img = cv2.GaussianBlur(img, (15, 15), 0)
        elif operation == "canny":
            img = cv2.Canny(img, 100, 200)
        elif operation == "sharpen":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img = cv2.filter2D(img, -1, kernel)
        elif operation == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
            img = cv2.transform(img, kernel)
        elif operation == "cartoon":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            smooth = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 250, 250)
            img = cv2.bitwise_and(color, color, mask=edges)
        elif operation == "invert":
            img = cv2.bitwise_not(img)
        else:
            raise ValueError("Invalid operation selected")
        
        cv2.imwrite(newFilename, img)
        return newFilename
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise

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
        try:
            operation = request.form.get("operation")
            if not operation or operation == "Choose an Operation":
                return render_template("error.html", 
                    error_title="Invalid Operation",
                    error_message="Please select a valid operation from the dropdown menu.")

            if 'file' not in request.files:
                return render_template("error.html",
                    error_title="No File Selected",
                    error_message="Please select a file to upload.")

            file = request.files['file']
            if file.filename == '':
                return render_template("error.html",
                    error_title="No File Selected",
                    error_message="Please select a file to upload.")

            if not allowed_file(file.filename):
                return render_template("error.html",
                    error_title="Invalid File Type",
                    error_message=f"Please upload a valid image file. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            try:
                new = processImage(filename, operation)
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
                return redirect(url_for('home'))
            except Exception as e:
                return render_template("error.html",
                    error_title="Processing Error",
                    error_message=f"An error occurred while processing your image: {str(e)}")

        except RequestEntityTooLarge:
            return render_template("error.html",
                error_title="File Too Large",
                error_message=f"Please upload a file smaller than {MAX_FILE_SIZE/1024/1024}MB")
        except Exception as e:
            return render_template("error.html",
                error_title="Unexpected Error",
                error_message="An unexpected error occurred. Please try again.")

    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html",
        error_title="Page Not Found",
        error_message="The page you are looking for does not exist."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html",
        error_title="Internal Server Error",
        error_message="Something went wrong on our end. Please try again later."), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
