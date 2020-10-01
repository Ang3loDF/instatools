from selenium import webdriver
from time import sleep

# get the number of following of a user
def following_count_of(driver, user):

    # get the user profile page
    driver.get("https://www.instagram.com/" + user)
    sleep(2)

    # initialize the count
    count = None

    # get count if the account is public
    try:
        count = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace(".", "")
    # get count if the account is private
    except:
        count = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/span/span").text.replace(".", "")
    
    try:
        count = int(count)
    except:
        count = None
    
    # return the count
    # if something went wrong or the user doesn't exist, return None
    return count