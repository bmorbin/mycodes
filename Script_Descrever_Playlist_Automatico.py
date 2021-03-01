# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:46:36 2021

@author: Bruno
"""
class Tempo:
    def __init__(self,duracao):
        ss_mm_hh=[]
        num = ''
        reverse_duracao = list(reversed(duracao))
        for l in reverse_duracao:
            if l != ":":
                num+=l
            else:
                new_num=''
                reverse_num=list(reversed(num))
                for char in reverse_num:
                    new_num += char
                ss_mm_hh+=[new_num]
                num=''
        new_num=''
        reverse_num=list(reversed(num))
        for char in reverse_num:
            new_num += char        
        ss_mm_hh+=[new_num]
        try: self.s = ss_mm_hh[0]
        except: self.s = str(00)
        try: self.min = ss_mm_hh[1]
        except: self.min = str(00)
        try: self.h = ss_mm_hh[2]
        except: self.h = str(00)
        
    def ajuste(self):
        return self.h+':'+self.min+':'+self.s

def pub(driver):
    try: 
        try:pub = driver.find_element_by_xpath('//*[@id="skip-button:6"]/span/button')
        except:pub = driver.find_element_by_xpath('//*[@id="skip-button:t"]/span/button')
        pub.click()
    except: 
        None

def pause(driver):
    try: 
        return driver.find_element_by_xpath('//*[@id="movie_player"]/div[28]/div[2]/div[1]/button')
    except: 
        try: 
            driver.find_element_by_xpath('//*[@id="dismiss-button"]/a').click()
            sleep(3)
        except:
            try: 
                return driver.find_element_by_xpath('//*[@id="movie_player"]/div[33]/div[2]/div[1]/button')
            except: 
                try: return driver.find_element_by_xpath('//*[@id="movie_player"]/div[35]/div[2]/div[1]/button')
                except: None
        try: return driver.find_element_by_xpath('//*[@id="movie_player"]/div[34]/div[2]/div[1]/button')
        except:
            sleep(2)
            pub(driver)
            sleep(5)
            return pause(driver)

from selenium import webdriver
from time import sleep

import pandas as pd
import numpy as np

PATH = 'C:/Users/Bruno/Desktop/chromedriver.exe'
url = 'https://www.youtube.com/playlist?list=PLxjKFMYkZ9OebLP0fskpz_aPYLHIfU9N6'
driver = webdriver.Chrome(PATH)
driver.get(url)

sleep(5)

playlist_name = driver.find_element_by_xpath('//*[@id="title"]/yt-formatted-string/a').text
button = driver.find_element_by_class_name('style-scope ytd-thumbnail-overlay-side-panel-renderer')
button.click()

sleep(5)

pause(driver).click()
aulas = driver.find_element_by_xpath('//*[@id="publisher-container"]/div/yt-formatted-string/span[3]').text
aula = driver.find_element_by_xpath('//*[@id="publisher-container"]/div/yt-formatted-string/span[1]').text
nome = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
# try: tempo = driver.find_element_by_xpath('//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
# except: tempo = driver.find_element_by_xpath('//*[@id="movie_player"]/div[34]/div[2]/div[1]/div[1]/span[3]').text
tempo = driver.find_element_by_class_name('ytp-time-duration').text
tempo_ajuste = Tempo(tempo)
tempo=tempo_ajuste.ajuste()

link = driver.current_url

print(aula)
print(nome)
print(tempo)
print(link)
print()

data = []
data += [[aula,nome,tempo,link]]

while int(aula)<int(aulas):
    try: next_button = driver.find_element_by_xpath('//*[@id="movie_player"]/div[28]/div[2]/div[1]/a[2]')
    except: 
        try: next_button = driver.find_element_by_xpath('//*[@id="movie_player"]/div[33]/div[2]/div[1]/a[2]')
        except: 
            try: next_button = driver.find_element_by_xpath('//*[@id="movie_player"]/div[34]/div[2]/div[1]/a[2]')
            except: next_button = driver.find_element_by_xpath('//*[@id="movie_player"]/div[35]/div[2]/div[1]/a[2]')
    next_button.click()
    
    sleep(5)
    
    pause(driver).click()
    aula = driver.find_element_by_xpath('//*[@id="publisher-container"]/div/yt-formatted-string/span[1]').text
    nome = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
    # try: tempo = driver.find_element_by_xpath('//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
    # except: tempo = driver.find_element_by_xpath('//*[@id="movie_player"]/div[34]/div[2]/div[1]/div[1]/span[3]').text
    tempo = driver.find_element_by_class_name('ytp-time-duration').text
    tempo_ajuste = Tempo(tempo)
    tempo=tempo_ajuste.ajuste()
    link = driver.current_url
    
    print(aula)
    print(nome)
    print(tempo)
    print(link)
    print()
    data += [[aula,nome,tempo,link]]

driver.quit()

df = pd.DataFrame(data=np.array(data),
                  columns = ['Aula','Nome','Duração','Link'])

df['Já visto'] = [False]*int(aulas)
df = df[['Já visto','Aula','Nome','Duração','Link']]

print(df.head(int(aulas)))

df.to_csv(playlist_name+'.csv',index=False)



