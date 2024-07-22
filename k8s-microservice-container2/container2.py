import logging
import os
from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

DATA_PATH = "../poojitha_PV_dir"  

def validate_json(data):
    if data is None or 'file' not in data or not isinstance(data['file'], str) or data['file'] == '':
        return False
    return True


def checking_csv_file_format(file_name):
    required_fields = ['product', 'amount']
    filepath = os.path.join(DATA_PATH, file_name)

    try:
        with open(filepath, 'r') as file:
            csv_reader = csv.DictReader(file)
            content = file.read().strip()

            if not content.startswith("product, amount"):
                return False
            
            for row in enumerate(csv_reader, start=2):
                if len(row) != len(required_fields):
                    return False

                if set(row.keys()) != set(required_fields):
                    return False 

                if any(not row[column] for column in required_fields):
                    return False

                try:
                    int(row['amount'])
                except ValueError:
                    return False

                if any(not row[column] for column in required_fields):
                    return False

        return True

    except FileNotFoundError:
        return False


def calculate_sum(file_name, product):
    total_sum = 0
    filepath = os.path.join(DATA_PATH, file_name)

    with open(filepath, 'r') as file:
        content_of_file = file.read().strip().split('\n')
        headers = content_of_file[0].split(', ')
        if 'amount' not in headers:
            return "0"

        amount_index = headers.index('amount')

        for line in content_of_file[1:]:
            columns = line.split(',')
            if len(columns) > amount_index:
                amount_value = columns[amount_index].strip()
                if amount_value:
                    try:
                        amt = int(amount_value)
                        if columns[0] == product:
                            total_sum += amt
                    except ValueError:
                        continue

    return str(total_sum)


@app.route('/processSum', methods=['POST'])
def processSum():
    data = request.get_json()
    file_name = data['file']
    product = data['product']

    try:
        if not checking_csv_file_format(file_name):
            error_response = {
                'file': file_name,
                'error': 'Input file not in CSV format.'
            }
            return jsonify(error_response), 400
        
        sum_value = calculate_sum(file_name, product)
        return jsonify({"file": file_name, "sum": int(sum_value)})

    except Exception as e:
        return jsonify({"file": file_name, "error": f"Error processing sum: {e}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)