
from flask import jsonify 
import pandas as pd

def get_contacts(df): 
    print(df)
    try: 
        results=[]
        phones,texts=df['phones'],df['text']
        for phone,text in zip(phones,texts): 
            phone = phone.strip() 
            text = text.strip()
            if not phone or not text:
                continue
            if not phone.startswith("+"):
                phone = "+91" + phone
            results.append({'phone':phone,'text':text})
        return results
    except Exception as e: 
        raise e
def parse_file(file):
    try: 
        file_name = file.filename.lower() 
        if file_name.endswith('.csv'): 
            df = pd.read_csv(file) 
        elif file_name.endswith('.xlsx'): 
            df = pd.read_excel(file, engine='openpyxl') 
        elif file_name.endswith('.xls'): 
            df = pd.read_excel(file) 
        else: 
            return jsonify({"error": "Unsupported file type"}), 400
        preview = df.head().to_dict(orient="records")
        return jsonify({
            "message": "File processed successfully",
            "preview": preview
        })
    except Exception as e:
        raise e

def parse_file_and_get_contacts(file):
    df = parse_file(file)
    results=get_contacts(df)
    return results