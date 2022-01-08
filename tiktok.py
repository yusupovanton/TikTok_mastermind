import ast

from TikTokAPI import TikTokAPI
import random
import os


def getrandom_fromos(folder):
    file_name = random.choice(os.listdir(folder))
    full_path = folder + file_name
    file = open(full_path, 'rb')
    return file, file_name
  

def filedelete(file_path, file_name):
    full_path = file_path + file_name
    os.remove(full_path)


def are_vids_low(folder):
    drive_files = os.listdir(folder)
    files_count = len(drive_files)
    if files_count <= 2:
        return True
    else:
        return False


def get_tiktok_vids(count, folder, register='tiktok_register.txt'):
    downloaded_set = set()
    api = TikTokAPI()
    
    retval = api.getTrending(count=count)

    with open(register, 'r') as file:
        if file.read():
            register_set = ast.literal_eval(file.read())
        else:
            print('The register is empty.')

    for item in retval.get('items'):

        id_ = item.get('id')
        if register_set:
            if id_ not in register_set:
                save_path = folder + '/file_vid' + str(id_) + '.mp4'
                api.downloadVideoById(id_, save_path)
                downloaded_set.add(id_)

            else:
                print(f'This ID has already been shown! id: {id_}')
        else:
            save_path = folder + '/file_vid' + str(id_) + '.mp4'
            api.downloadVideoById(id_, save_path)

        new_register_set = register_set.Union(downloaded_set)

        with open(register, 'w') as file:
            file.write(new_register_set)


        
