from selenium import webdriver
from time import sleep

from tools.followers_of import followers_of
from tools.following_of import following_of
from tools.returned_followers_ratio import returned_followers_ratio
from tools.followers_count_of import followers_count_of
from tools.following_count_of import following_count_of

""" 
Scraper class:
    - login and initialize driver
    - all the mothods required (get from tools)

"""

class Scraper:

    # initialize the finding process with the correct values.
    def __init__(self, username, psw, chrome_driver_path="C:\Program Files (x86)\chromedriver.exe"):

        # set variables
        self.PATH = chrome_driver_path

        # initialize the web driver
        try:
            self.driver = webdriver.Chrome(self.PATH)
        except:
            print("Error: something went wrong :( , check you have Chrome Driver installed or that the given path ("+ self.PATH +") is correct.")
            return None


        # launch the browser with instagram
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        
        # login
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(psw)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(7)

        # click not now
        try:
            self.driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[3]/button[2]").click()
            sleep(3)
        except:
            print("Error: something went wrong :( , check your credentials are correct.")


    # close the browser
        def close(self):
            self.driver.quit()

    
    # get the followers of a user
    def followers_of(self, user):
        return followers_of(self.driver, user)

    # get the following of a suer
    def following_of(self, user):
        return following_of(self.driver, user)


    # find the users of a list with the best ratio of returned followers
    # $max_lists_length - the max number of followers/following of a user of the list (we don't wont to scan celebrities)
    def returned_followers_ratio(self, users, max_lists_length=400):
        return returned_followers_ratio(self.driver, users, max_lists_length)
    

    # get the number of followers of a user
    def followers_count_of(self, user):
        return followers_count_of(self.driver, user)

    # get the number of following of a user
    def following_count_of(self, user):
        return following_count_of(self.driver, user)
