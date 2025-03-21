# Edit Monkey - Online Image Editor

Edit Monkey is a powerful yet simple web-based image editing tool that allows users to apply various image processing operations and format conversions to their images.

## Features

- 🖼 Image format conversion (PNG, JPG, WebP)
- 🎨 Image filters and effects:
  - Grayscale conversion
  - Sepia effect
  - Blur effect
  - Edge detection (Canny filter)
  - Image sharpening
  - Cartoon effect
  - Color inversion
- ⚡ Fast and efficient processing
- 📱 Responsive design for both desktop and mobile
- 🌙 Dark theme UI
- 🔒 Secure file handling
- ⚠️ Comprehensive error handling

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Image Processing**: OpenCV (cv2)
- **File Handling**: Werkzeug

## Prerequisites

- Python 3.7 or higher
- OpenCV (cv2)
- Flask
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/edit-monkey.git
cd edit-monkey
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create required directories:
```bash
mkdir uploads static
```

## Usage

1. Start the Flask server:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an image and select an operation from the dropdown menu.

4. Click "Process Image" to apply the selected operation.

5. Download your processed image from the provided link.

## File Size Limits

- Maximum file size: 10MB
- Supported formats: PNG, WebP, JPG, JPEG, GIF

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size limits
- Processing errors
- Server errors
- Page not found errors

## Project Structure

```
edit-monkey/
├── main.py              # Flask application
├── requirements.txt     # Python dependencies
├── static/             # Processed images
├── templates/          # HTML templates
│   ├── index.html     # Main page
│   ├── about.html     # About page
│   ├── how.html       # How to use page
│   └── error.html     # Error page
└── uploads/           # Temporary upload directory
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for image processing capabilities
- Bootstrap for the UI framework
- Font Awesome for icons

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/edit-monkey](https://github.com/yourusername/edit-monkey)
