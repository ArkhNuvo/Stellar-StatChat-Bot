from utility.callbackdata import UserData, DocInfo
import os


def collect_general_data(id, first_name):
    UserData.id = str(id)
    UserData.name = str(first_name)
    UserData.folder_path = f"data_bases/{id}"
    try:
        list_of_files = os.listdir(f"data_bases/{id}")
        UserData.file_count = len(list_of_files)
    except:
        return
    return 

def collect_doc_info(name, action):
    DocInfo.name = name
    DocInfo.action = action
