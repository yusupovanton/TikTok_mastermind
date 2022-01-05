from TikTokAPI import TikTokAPI
import random
import os
import telebot
import time


from config import BOT_API, CHANNEL_ID, MAINTENANCE_CH_ID, VIDS_FOLDER

bot = telebot.TeleBot(BOT_API)


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
        

def telegram_bot(folder):
    
    while True:
        try:
          if are_vids_low(folder):
              get_tiktok_vids(30, folder)

          file = getrandom_fromos(folder)[0]
          file_name = getrandom_fromos(folder)[1]
          
          bot.send_video(chat_id=CHANNEL_ID, data=file, supports_streaming=True)

          filedelete(folder, file_name)

          print('Video post successful, going to sleep now...')
          
        except Exception as ex:
          bot.send_message(chat_id=MAINTENANCE_CH_ID, message='Error in TikTokMM bot: ' + ex)
          
        finally:
          sleeptime = random.randint(1200, 2400)
          time.sleep(sleeptime)


        
def main():
    telegram_bot(VIDS_FOLDER)


if __name__ == '__main__':
    main()
