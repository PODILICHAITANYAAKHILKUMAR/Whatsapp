import pandas as pd
import yaml

def fetch_config():
    # Load YAML constants
    try:
        with open("constants.yaml", "r") as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        raise e
def get_contacts(contact_info): 
    try: 
        contacts=[]
        phones = list(contact_info['phones'].values())
        messages = list(contact_info['messages'].values())
        for phone,message in zip(phones,messages):
            phone = str(phone).strip() 
            message = message.strip()
            if not phone or not message:
                continue
            if not phone.startswith("+"):
                phone = "+91" + phone
            contacts.append({'phone':phone,'message':message})
        return contacts
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
        return df.to_dict()
    except Exception as e:
        raise e

def parse_file_and_get_contacts(file):
    df = parse_file(file)
    results=get_contacts(df)
    return results

CONFIG=fetch_config()