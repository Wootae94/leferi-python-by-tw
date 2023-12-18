import requests, json
import pandas as pd

NOTION_CONFIG_PATH = './.config/notion_auth.json'

def load_notion_config():
    with open(NOTION_CONFIG_PATH) as json_file:
        return json.load(json_file)

def get_notion_users():
    headers = load_notion_config()
    url = "https://api.notion.com/v1/users?page_size=100"

    res = requests.get(url, headers=headers)
    print(res.status_code)
    df = pd.DataFrame(data=res.json()["results"])
    return df


def read_notion_database(databaseId):
    headers = load_notion_config()
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    nextToken = ''
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    nextToken = data['results'][-1]['id']
    pageToken = nextToken
    print(res.status_code)
    notion_data_dict_list = []
    notion_data_dict_list += data['results']
    # 100개 이상인 경우, 다음 페이지 로드
    while len(data['results']) == 100:
        payload = {
            "start_cursor": f"{pageToken}"
        }
        res = requests.request("POST", readUrl, json=payload, headers=headers)
        data = res.json()
        nextToken = data['results'][-1]['id']
        pageToken = nextToken
        notion_data_dict_list += data['results']
        print(res.status_code)
    df = pd.DataFrame(data=notion_data_dict_list)
    return df


def create_notion_page(databaseId, properties):
    headers = load_notion_config()
    createUrl = "https://api.notion.com/v1/pages"

    newPageData = {
            "parent": {"database_id": databaseId},
            "properties": properties
        }

    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)

    if str(res.status_code) == '400':
        print(res.text)

def delete_notion_page(pageId):
    headers = load_notion_config()
    deleteUrl = f"https://api.notion.com/v1/pages/{pageId}"

    deletePayLoad = {
        "archived": True
    }

    res = requests.patch(deleteUrl, json=deletePayLoad, headers=headers)

    if str(res.status_code) == '400':
        print(res.text)


def update_notion_page(pageId,properties):
    headers = load_notion_config()
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"
    updateData = {
            "properties": properties
            }
    data = json.dumps(updateData)
    response = requests.request("PATCH",updateUrl,headers=headers,data=data)

    if str(response.status_code) == '400':
        print(response.text)
