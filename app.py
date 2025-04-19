from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder (temporary storage)
UPLOAD_FOLDER = 'workspace/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed audio extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_folder():
    if 'files' not in request.files:
        return jsonify({"error": "No files selected"}), 400
    
    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({"error": "Empty folder"}), 400

    audio_files = []
    for file in files:
        if file.filename == '':
            continue
            
        if allowed_file(file.filename):
            # Securely save the file temporarily
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            audio_files.append(filename)

    return jsonify({
        "success": True,
        "message": f"Processed {len(audio_files)} audio files",
        "audio_files": audio_files
    })

if __name__ == '__main__':
    app.run(debug=True)