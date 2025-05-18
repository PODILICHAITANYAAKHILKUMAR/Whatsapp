
import pandas as pd

def get_contacts(df): 
    print(df)
    try: 
        results=[]
        phones,messages=df['phones'],df['messages']
        for phone,message in zip(phones,messages): 
            phone = phone.strip() 
            message = message.strip()
            if not phone or not message:
                continue
            if not phone.startswith("+"):
                phone = "+91" + phone
            results.append({'phone':phone,'message':message})
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
            return pd.DataFrame()
        return df.head().to_dict(orient="records")
    except Exception as e:
        raise e

def parse_file_and_get_contacts(file):
    df = parse_file(file)
    results=get_contacts(df)
    return results