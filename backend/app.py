import os 
from flask import Flask, request, jsonify 
from flask_cors import CORS 
import requests 
from dotenv import load_dotenv 
from utils import parse_file_and_get_contacts

load_dotenv()

app = Flask(__name__) 
CORS(app)

ACCESS_TOKEN = os.getenv('WHATSAPP_TOKEN') 
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

API_VERSION = 'v19.0'
API_URL = f"https://graph.facebook.com/{PHONE_NUMBER_ID}/messages"

headers = { "Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json" }

@app.route('/') 
def home(): 
    return 'Sever Running'

@app.route('/send_messages', methods=['POST']) 
def send_messages(): 
    try:
        contacts=parse_file_and_get_contacts(request.files.get('file'))
        results=[]
        for contact in contacts:
            phone,text=contact['phone'],contact['text']
            payload = {
                    "messaging_product": "whatsapp",
                    "to": phone,
                    "type": "text",
                    "text": {
                        "body": text
                    }
                }
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                results.append({"number": phone, 'text':text,"status": "sent"})
            else:
                results.append({
                        "number": phone,
                        'text':text,
                        "status": "error",
                        "detail": response.text
                    })
        return jsonify({"message": "Messages processed", "results": results})
    except Exception as e:
        raise e
if __name__ == '__main__':
    app.run(port=5000,debug=True)