from selenium import webdriver
from time import sleep

# It has some tools to find the percentage of the followers that have been reciprocated
# by users in a list of instagram users.

class ReturnedFollowersRatio:

    # initialize the finding process with the correct values.
    def __init__(self, username, psw, chrome_driver_path="C:\Program Files (x86)\chromedriver.exe", max_lists_length=400):

        # set variables
        self.PATH = chrome_driver_path
        self.max_lists_length = max_lists_length

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
        sleep(3)

        # click not now
        try:
            self.driver.find_element_by_xpath("html/body/div[1]/section/main/div/div/div/div/button").click()
            sleep(3)
            self.driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[3]/button[2]").click()
            sleep(3)
        except:
            print("Error: something went wrong :( , check your credentials are correct.")

    

    # close the browser
    def close(self):
        self.driver.quit()



    # get a users list from the followers of a specified user
    def find_list_from_followers(self, user):
        print("Finding the user list from followers of " + user + "...")

        # get the user's profile page
        self.driver.get("https://www.instagram.com/" + user)
        sleep(2)

        # find the follower of the user
        user_list = self.get_followers_list(user)

        return user_list



    # launch the searching process. Find the percentage of returned follower for every user in the
    # list and sort them from highest to lowest
    def search_list(self, user_list):
        
        # define the list
        users_ratios = [None] * len(user_list)

        print("Scanning the users of the list...")

        # for every user compare the followers to following and add to the list
        for i in range(len(user_list)):
            print("User " + str(i) + " of " + str(len(user_list)) + " scanning - " + user_list[i])
            ratio = self.search_user(user_list[i])
            users_ratios[i] = {"name": user_list[i], "return_ratio": ratio}

        # sorting function - for every user get the return_ratio value
        def sortingKey(e):
            return e["return_ratio"]

        # sort from the highest with the sorting function
        users_ratios.sort(key=sortingKey, reverse=True)

        return users_ratios


    
    # find the percentage of returned follower for a single user
    def search_user(self, user):
        
        # get the user's profile page
        self.driver.get("https://www.instagram.com/" + user)
        sleep(2)

        # if has too much followers/following return -1
        if (not self.is_followers_list_short(user)) or (not self.is_following_list_short(user)):
            return -1.0

        # get the followers and the following lists
        followers = self.get_followers_list(user)
        sleep(1)
        following = self.get_following_list(user)

        # if the account is private return 0
        if followers == None or following == None:
            return 0

        # count the returned followers
        returned_following_count = 0
        for follower in followers:
            if follower in following:
                returned_following_count += 1
        
        # calculate the percentage
        ratio = returned_following_count / len(followers)

        return ratio



    # get the list of followers for a single user
    def get_followers_list(self, user):
        
        # click on the followers link
        try:
            self.driver.find_element_by_xpath("//a[@href='/" + user + "/followers/']").click()
        except:
            # the account is private
            return None
        sleep(2)

        # get the scrolling box
        scroll_box = self.driver.find_element_by_xpath("html/body/div[4]/div/div/div[2]")

        # scroll until every follower is loaded
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;", scroll_box)

        # get the followers' names
        links = scroll_box.find_elements_by_tag_name("a")
        names = [name.text for name in links if name.text != ""]
        
        # close follower window
        self.driver.find_element_by_xpath("html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        
        return names
    


    def get_following_list(self, user):
        
        # click on the following link
        try:
            self.driver.find_element_by_xpath("//a[@href='/" + user + "/following/']").click()
        except:
            # the account is private
            return None
        sleep(2)

        # get the scrolling box 
        scroll_box = self.driver.find_element_by_xpath("html/body/div[4]/div/div/div[2]")

        # scroll until every following is loaded
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;", scroll_box)

        # get the following names
        links = scroll_box.find_elements_by_tag_name("a")
        names = [name.text for name in links if name.text != ""]
        
        # close following window
        self.driver.find_element_by_xpath("html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        
        return names



    # check if the followers number is small enough 
    def is_followers_list_short(self, user):
        
        # get the number of followers
        try:
            # if the account is not private
            followers_num_str = self.driver.find_element_by_xpath("//a[@href='/" + user + "/followers/']/span").text.replace(".", "")
        except: 
            # if the account is private
            followers_num_str = self.driver.find_element_by_xpath("html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span").text.replace(".", "")
        
        # convert the number of followers to int
        try:
            followers_num = int(followers_num_str)
        except:
            return False

        # check the number of follower is smaller than the max list length
        if followers_num > self.max_lists_length:
            return False
        return True

    

    # check if the following number is small enough 
    def is_following_list_short(self, user):

        # get the number of following
        try:
            # if the account is not private
            following_num_str = self.driver.find_element_by_xpath("//a[@href='/" + user + "/following/']/span").text.replace(".", "")
        except:
            # if the account is private
            following_num_str = self.driver.find_element_by_xpath("html/body/div[1]/section/main/div/header/section/ul/li[3]/span/span").text.replace(".", "")
        
        # convert the number of following to int
        try:
            following_num = int(following_num_str)
        except:
            return False
        
        # check the number of following is smaller than the max list length
        if following_num > self.max_lists_length:
            return False
        return True