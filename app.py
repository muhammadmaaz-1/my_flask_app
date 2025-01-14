from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
import os
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/currency')
def currency():
    return render_template('currency.html')

@app.route('/unit')
def unit():
    return render_template('unit.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/save_pdf', methods=['POST'])
def save_pdf():
    content = request.form.get('content')  # Fixed the missing import issue
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, content)

    output_path = os.path.join('static', 'output.pdf')
    pdf.output(output_path)

    return send_file(output_path, as_attachment=True)

API_KEY = '2bede587d31401ecdaef5639' 
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    try:
        response = requests.get(API_URL)
        data = response.json()
        if data['result'] == 'success':
            currencies = data['conversion_rates']
            return jsonify(currencies)
        else:
            return jsonify({'error': 'Error fetching currency data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/convert', methods=['GET'])
def convert_currency():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = float(request.args.get('amount'))

    try:
        response = requests.get(API_URL)
        data = response.json()

        if data['result'] == 'success':
            conversion_rates = data['conversion_rates']
            conversion_rate = conversion_rates[to_currency] / conversion_rates[from_currency]
            result = round(amount * conversion_rate, 2)
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Error fetching conversion data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
