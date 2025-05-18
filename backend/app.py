import os 
from flask import Flask, request, jsonify 
from flask_cors import CORS 
import requests 
from dotenv import load_dotenv 
from utils import parse_file_and_get_contacts,CONFIG

load_dotenv()

app = Flask(__name__) 
CORS(app)

ACCESS_TOKEN = os.getenv('WHATSAPP_TOKEN') 
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

API_URL = CONFIG['API_URL'].format(PHONE_NUMBER_ID=PHONE_NUMBER_ID)

headers = { "Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json" }

@app.route('/') 
def home(): 
    return 'Sever Running at {}'

@app.route('/send_messages', methods=['POST']) 
def send_messages(): 
    try:
        contacts=parse_file_and_get_contacts(request.files.get('file'))
        results=[]
        for contact in contacts:
            phone,message=contact['phone'],contact['message']
            payload = {
                    "messaging_product": "whatsapp",
                    "to": phone,
                    "type": "text",
                    "text": {
                        "body": message
                    }
                }
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                results.append({"number": phone, 'message':message,"status": "sent"})
            else:
                results.append({
                        "number": phone,
                        'message':message,
                        "status": "error",
                        "detail": response.text
                    })
        return jsonify({"message": "Messages processed", "results": results})
    except Exception as e:
        raise e
if __name__ == '__main__':
    app.run(port=CONFIG['SERVER_PORT'],debug=CONFIG['SERVER_DEBUG_MODE'])