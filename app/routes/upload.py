from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.services.loader import process_csv

upload_bp = Blueprint('upload',__name__)
UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload/<table_name>', methods=['POST'])
def upload_csv(table_name):
    if table_name not in ['departments','jobs','hired_employees']:
        return jsonify({'error':'Invalid table name'}), 400

    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        return jsonify({'error':'No valid CSV uploaded'}), 400
    
    # save file in tmp folder
    print(f'saving file in folder {UPLOAD_FOLDER}...')
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(f'file save suceeded')

    try:
        result = process_csv(filepath, table_name)
        
        if result['inserted_count'] == 0:
            return jsonify({
                'message': f"No new records inserted into '{table_name}' — all records already exist.",
                'skipped_duplicates': result['skipped_duplicates']
            }), 200

        return jsonify({
            'message': f'{result["inserted_count"]} records inserted into {table_name}',
            'skipped_duplicates':result['skipped_duplicates']
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500