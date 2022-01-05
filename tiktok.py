from TikTokAPI import TikTokAPI
import random
import os
import telebot
import time

from config import API_TOKEN, CHANNEL_ID, MAINTENANCE_CH_ID, VIDS_FOLDER


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


def get_tiktok_vids(count, folder):

    api = TikTokAPI()
    
    retval = api.getTrending(count=count)
    i = 1

    for item in retval.get('items'):

        save_path = folder + '/file_vid' + str(i) + '.mp4'
        id = item.get('id')

        api.downloadVideoById(id, save_path)
        i += 1
        
