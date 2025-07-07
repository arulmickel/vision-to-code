from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from image_to_html import convert_image_to_html

UPLOAD_FOLDER = 'web_uploads'
OUTPUT_FOLDER = 'web_outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                # Generate HTML
                output_dir = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(filename)[0])
                html_path = convert_image_to_html(upload_path, output_dir)
                return redirect(url_for('result', output_folder=os.path.basename(output_dir)))
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a PNG, JPG, JPEG, or GIF file.', 'error')
            return redirect(request.url)
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>UI2HTML Web Interface</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .upload-form {
                    text-align: center;
                    margin: 20px 0;
                }
                .file-input {
                    margin: 20px 0;
                }
                .submit-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                .submit-btn:hover {
                    background-color: #45a049;
                }
                .flash-messages {
                    margin: 20px 0;
                }
                .flash-message {
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                }
                .error {
                    background-color: #ffebee;
                    color: #c62828;
                    border: 1px solid #ffcdd2;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>UI2HTML Web Interface</h1>
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        <div class="flash-messages">
                            {% for category, message in messages %}
                                <div class="flash-message {{ category }}">{{ message }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endwith %}
                <div class="upload-form">
                    <form method="post" enctype="multipart/form-data">
                        <div class="file-input">
                            <input type="file" name="file" accept="image/*" required>
                        </div>
                        <input type="submit" value="Convert to HTML" class="submit-btn">
                    </form>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/result/<output_folder>')
def result(output_folder):
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], output_folder)
    html_path = os.path.join(output_dir, 'index.html')
    image_path = os.path.join(output_dir, 'frame.jpg')
    
    if not os.path.exists(html_path):
        flash('HTML output not found', 'error')
        return redirect(url_for('upload_file'))
        
    try:
        with open(html_path, encoding='utf-8') as f:
            html_content = f.read()
            
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>UI2HTML Result</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #333;
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .result-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 20px;
                        align-items: flex-start;
                    }
                    .image-section {
                        flex: 0 0 300px;
                        max-width: 30%;
                        text-align: center;
                    }
                    .html-section {
                        flex: 1 1 100%;
                    }
                    .image-section img {
                        max-width: 100%;
                        height: 200px;
                        object-fit: contain;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .html-section iframe {
                        width: 100%;
                        height: 500px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .back-link {
                        display: block;
                        text-align: center;
                        margin-top: 20px;
                        color: #4CAF50;
                        text-decoration: none;
                    }
                    .back-link:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Generated HTML Result</h1>
                    <div class="result-container">
                        <div class="image-section">
                            <h2>Original Image</h2>
                            <img src="{{ url_for('output_file', output_folder=output_folder, filename='frame.jpg') }}" alt="Original UI">
                        </div>
                        <div class="image-section">
                            <h2>Grayscale Image</h2>
                            <img src="{{ url_for('output_file', output_folder=output_folder, filename='grayscale_frame.jpg') }}" alt="Grayscale UI">
                        </div>
                        <div class="image-section">
                            <h2>Detected Components</h2>
                            <img src="{{ url_for('output_file', output_folder=output_folder, filename='detected_components.jpg') }}" alt="Detected Components">
                        </div>
                        <div class="html-section">
                            <h2>HTML Output</h2>
                            <iframe src="{{ url_for('output_file', output_folder=output_folder, filename='index.html') }}"></iframe>
                        </div>
                    </div>
                    <a href="/" class="back-link">← Try another image</a>
                </div>
            </body>
            </html>
        ''', html_content=html_content, output_folder=output_folder)
    except Exception as e:
        flash(f'Error displaying result: {str(e)}', 'error')
        return redirect(url_for('upload_file'))

@app.route('/output/<output_folder>/<filename>')
def output_file(output_folder, filename):
    return send_from_directory(os.path.join(app.config['OUTPUT_FOLDER'], output_folder), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 