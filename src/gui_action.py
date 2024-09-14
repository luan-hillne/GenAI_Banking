# from config_app.model_config import LoadConfig
import datetime, time, os
from src.utils.model_settings import Model_Settings
from src.utils.prompts import system_message_prompt
model_settings = Model_Settings()

def btn_save_click(txt_system_prompt):
    model_settings.SYSTEM_PROMPT = txt_system_prompt
    print("\nsystem_prompt:",model_settings.SYSTEM_PROMPT)
    
def btn_reset_click(txt_system_prompt):
    model_settings.SYSTEM_PROMPT = system_message_prompt
    return model_settings.SYSTEM_PROMPT

def btn_save_workspace_click(workspace_list):
    # my_platform = platform.system() #  "Linux", "Windows", or "Darwin" (Mac)
    folder_path = "data/chat_workspaces"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # current date and time
    now = datetime.now()
    time_now = now.strftime("%Y-%m-%d_%H-%M-%S")

    for wp in workspace_list:
        file_name = str(time_now)+"_"+str(wp["id"])+"_"+str(wp["name"])+'.txt'

        file_path = ""
        # if my_platform == "Windows":
        #     file_path = folder_path + "\\" + file_name
        # elif my_platform == "Darwin":
        #    file_path = folder_path + "/" + file_name
        # else:
        file_path = folder_path + "/" + file_name

        with open(file_path, 'w', encoding="utf-8") as f:
            for chat in wp["history"]:
                f.write(str(chat[0])+"\n"+str(chat[1])+"\n\n")
        print("\nsave workspace to ~>",file_path)
    
def btn_create_new_workspace_click(workspace_list):
    max_id = 0
    for wp in workspace_list:
        if wp["id"] >= max_id:
            max_id = wp["id"] + 1
    workspace = {"id":max_id, "name":"New workspace "+str(max_id), "history":[["**human**: Hello", "**Jarvis (AI)**: Hi, my name Raffles. I am your assistant. How may I help you today?  [v{0}]".format(max_id)]]}
    workspace_list.insert(0, workspace)
    return workspace_list, workspace