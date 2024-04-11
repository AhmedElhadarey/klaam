from flask import Flask, request, jsonify
import tempfile
import os
from klaam import SpeechRecognition

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Save the uploaded file to a temporary path
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)
        # File received, now send it to Klaam for transcription
        transcribed_text = transcribe(temp_file_path)
        # Remove temporary file and directory
        os.remove(temp_file_path)
        os.rmdir(temp_dir)
        return jsonify({'transcribed_text': transcribed_text})
    except Exception as e:
        return jsonify({'error': str(e)})

    

def transcribe(audio_path):
    model = SpeechRecognition()
    model.transcribe(audio_path)
if __name__ == '__main__':
    app.run(debug=True)  # Run Flask server in debug mode
