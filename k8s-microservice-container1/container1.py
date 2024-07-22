from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CONTAINER_2_ENDPOINT_SUM = 'http://localhost:4000/processSum'
STORAGE_PATH = "../poojitha_PV_dir"  

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    if 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_content = data.get('data', '').replace(' ', '')

    lines = file_content.split('\n')

    if lines:
        lines[0] = lines[0].replace(',', ', ')

    formatted_content = '\n'.join(lines)

    try:
        os.makedirs(STORAGE_PATH, exist_ok=True)
        file_path = os.path.join(STORAGE_PATH, data['file'])  
        with open(file_path, 'w') as file:
            file.write(formatted_content)
        return jsonify({"file": data['file'], "message": "Success."})
    except Exception as e:
        return jsonify({"file": data['file'], "error": f"Error while storing the file to the storage: {e}"}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    if 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    file_path = os.path.join(STORAGE_PATH, data['file'])
    if not os.path.exists(file_path):
        return jsonify({"file": data["file"], "error": "File not found."}), 404

    try:
        response = requests.post(CONTAINER_2_ENDPOINT_SUM, json=data)
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)