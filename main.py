from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/get-otp', methods=['GET'])
def get_otp():
    page_url = request.args.get('url')
    if not page_url:
        return jsonify({"error": "URL is required as ?url=..."})

    try:
        response = requests.get(page_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        possible_code = soup.find(string=re.compile(r'\b\d{6}\b'))
        if not possible_code:
            return jsonify({"error": "OTP code not found on the page"}), 404
        otp_match = re.search(r'\b\d{6}\b', possible_code)
        if otp_match:
            otp = otp_match.group()
            return jsonify({"otp": otp, "source_url": page_url})
        return jsonify({"error": "OTP code not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
