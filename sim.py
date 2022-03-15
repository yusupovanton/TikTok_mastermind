import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

input_ = 'vk'


class Scraper:

    """Scraping sims"""

    def __init__(self):
        self.options = Options()
        self.options.add_argument("-profile")
        self.options.add_argument("/Users/yustas/Library/Application Support/Firefox/Profiles/fls5updd.default-release-1")
        self.driver = webdriver.Firefox(options=self.options)

    def get_url(self):

        dr = self.driver
        try:

            dr.get('https://onlinesim.ru/v2/receive/sms')
            time.sleep(3)
            search = dr.find_element(By.XPATH,
                                     '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div')
            search.click()
            search = dr.find_element(By.XPATH,
                                     '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div/input')
            search.send_keys(input_)
            time.sleep(3)
            vars = dr.find_elements(By.CLASS_NAME, 'service-item-text')

            for item in vars:
                text = item.text
                print(text)
            choice = str(input('Choose one of the options above ^'))
            search = dr.find_element(By.XPATH,
                                     '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div')
            search.click()

            search = dr.find_element(By.XPATH,
                                     '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div/input')
            search.clear()
            search.send_keys(choice)
            answer = str(input('Confirm Buy?'))

            if answer.lower() == 'yes':
                print('Your answer was yes')
                dr.find_element(By.CLASS_NAME, 'service-item-text').click()
                dr.find_element(By.XPATH,
                                '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/ul[1]/li/button').click()
                element = WebDriverWait(dr, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'media-body')))
                while True:
                    sms = dr.find_elements(By.CLASS_NAME, 'media-body')
                    for item in sms:

                        print(item.text)
        except Exception as ex:
            print(ex)

        finally:
            breakpoint()
            dr.close()


if __name__ == '__main__':
    Scraper().get_url()
