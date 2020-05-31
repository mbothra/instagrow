from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def main():
    chromedriver_path = '/usr/local/bin/chromedriver' # Change this to your own chromedriver path!
    web_driver = webdriver.Chrome(executable_path=chromedriver_path)
    sleep(4)
    web_driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(6)

    username = web_driver.find_element_by_name('username')
    username.send_keys('ammara_fashion_kolkata')
    password = web_driver.find_element_by_name('password')
    password.send_keys('shova@63')

    button_login = web_driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
    button_login.click()
    sleep(6)

    notnow = web_driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow.click()

    hashtag_list = ['fashiondesigner', 'fashion', 'fashionblogger', 'fashionista', 
      'style', 'designer', 'fashionstyle', 'instafashion', 'fashiondesign','kolkatafashion', 'fashionable','fashionweek', 'fashionshow', 'fashiongram','fashionaddict', 'fashionlover', 'fashionnova', 'fashionistas', 'indiancouture', 'indianwear','couture','indowestern', 'zardozi', 'ethnicwear', 'bride', 'bridalwear', 'bridesmaids',
     'ashiondesignerindia', 'fashiondesignersby', 'fashiondesignermumbai', 'fashiondesignerextraordinaire', 'fashiondesignerkolkata', 'weddingispo', 'weddinginspiration', 'bridesmaidoutfit']

    prev_user_list = []
    # if it's the first time you run it, use this line and comment the two below
    prev_user_list = pd.read_csv('20200220-152703_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
    prev_user_list = list(prev_user_list['0'])

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hashtag in hashtag_list:
        tag += 1
        web_driver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
        sleep(5)
        first_thumbnail = web_driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
        
        first_thumbnail.click()
        sleep(randint(1,2))    
        try:        
            for x in range(1,10000):
                username = web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
                print(username)
                if username not in prev_user_list:
                    # If we already follow, do not unfollow
                    if web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                        print("Trying to Follow")
                        web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                        print("Followed")
                        new_followed.append(username)
                        followed += 1

                        # Liking the picture
                        button_like = web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                        button_like.click()
                        print("Liked")
                        likes += 1
                        sleep(randint(18,25))

                        # Comments and tracker
                        comm_prob = randint(4,10)
                        print('{}_{}: {}'.format(hashtag, x,comm_prob))
                        if comm_prob > 6:
                            comments += 1
                            web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button').click()
                            print("Commenting")
                            comment_box = web_driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                            # if (comm_prob < 7):
                            #     comment_box.send_keys('Really cool!')
                            #     sleep(1)
                            if (comm_prob > 6) and (comm_prob < 9):
                                comment_box.send_keys('In awe :)')
                                sleep(1)
                            elif comm_prob == 9:
                                comment_box.send_keys('Wow! Amazing stuff!')
                                sleep(1)
                            elif comm_prob == 10:
                                comment_box.send_keys('So cool! :)')
                                sleep(1)
                            # Enter to post comment
                            comment_box.send_keys(Keys.ENTER)
                            sleep(randint(22,28))

                    # Next picture
                    web_driver.find_element_by_link_text('Next').click()
                    sleep(randint(10,20))
                else:
                    web_driver.find_element_by_link_text('Next').click()
                    sleep(randint(10,20))
        # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
        except:
            continue

    for n in range(0,len(new_followed)):
        prev_user_list.append(new_followed[n])
        
    updated_user_df = pd.DataFrame(prev_user_list)
    updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
    print('Liked {} photos.'.format(likes))
    print('Commented {} photos.'.format(comments))
    print('Followed {} new people.'.format(followed))

def scroll_follower_list(elem, follower):
    print('scrolling')
    elem.send_keys(Keys.END)


def follow_the_followers():
    users_list = ['bhagyashree_rajput']

    chromedriver_path = '/usr/local/bin/chromedriver' # Change this to your own chromedriver path!
    web_driver = webdriver.Chrome(ChromeDriverManager().install())
    sleep(6)
    web_driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(6)

    username = web_driver.find_element_by_name('username')
    username.send_keys('ammara_fashion_kolkata')
    password = web_driver.find_element_by_name('password')
    password.send_keys('shova@63')

    button_login = web_driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
    button_login.click()
    sleep(6)

    save_info = web_driver.find_element_by_css_selector('#react-root > section > main > div > div > div > section > div > button')
    save_info.click()

    sleep(3)
    notnow = web_driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow.click()
    follower = 1
    for user in users_list:
        web_driver.get('https://www.instagram.com/'+ user + '/')
        sleep(5)
        followers_button_text = web_driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').text
        no_of_followers = followers_button_text[0:followers_button_text.index(' ')].replace(',','')
        formatted_followers = convert_to_number(no_of_followers)
        web_driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        sleep(4)
        use_alt = False
        
        while follower < formatted_followers:
            try:
                if use_alt:
                    elem = web_driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li['+str(follower)+']/div/div[2]/button')
                else:
                    elem = web_driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li['+str(follower)+']/div/div[3]/button')
                if elem.text == 'Follow':
                    sleep(4)
                    if use_alt:
                        username = web_driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li['+str(follower)+']/div/div[1]/div[2]/div[1]/a')
                    else:
                        username = web_driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li['+str(follower)+']/div/div[2]/div[1]/div/div/a')
                    username = username.text
                    print("Trying to Follow user - ",username)
                    sleep(2)
                    elem.click()
                    print("Followed")
            except NoSuchElementException as e:
                print(e)
                use_alt=True
                follower = follower - 1
                scroll_follower_list(elem, follower)
            follower = follower+1

def convert_to_number(number_str):
    if 'k' in number_str:
        return round(float(number_str[:len(number_str)-1]),0)*1000 
    elif 'm' in number_str:
        return round(float(number_str[:len(number_str)-1]),0)*1000000
    else:
        return int(number_str)

if __name__ == '__main__':
    follow_the_followers()
