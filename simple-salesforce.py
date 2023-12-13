import json

from simple_salesforce import Salesforce
import requests
import pandas as pd

SALESFORCE_CONFIG_PATH = './.config/simple_salesforce_auth.json'
def load_salesforce_config():
    with open(SALESFORCE_CONFIG_PATH) as json_file:
        return json.load(json_file)

def connect_to_salesforce():
    config_json = load_salesforce_config()
    session = requests.Session()
    sf = Salesforce(username=config_json['username'],password=config_json['password'],organizationId=config_json['organizationId'],session=session)
    return sf

def select_account_id_from_salesforce():
    sf = connect_to_salesforce()
    # 쿼리문 참조 : https://simple-salesforce.readthedocs.io/en/latest/user_guide/queries.html
    dict = sf.query("SELECT ID FROM ACCOUNT where RecordTypeId = '0122w0000000YBcAAM'")
    sf_cre_df = pd.DataFrame(data=dict['records'])
    sf_cre_df.columns = ['attr', 'ID']
    print(sf_cre_df)

if __name__ == '__main__':
    select_account_id_from_salesforce()