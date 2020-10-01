from selenium import webdriver
from time import sleep
from tools.followers_of import followers_of
from tools.following_of import following_of

# get the followers of a user that don't return the follow
# if $returned, get the list of the returned followers, else of the not-returned followers
def returned_followers(driver, user, returned=True):
    
    # get the user's profile page
    driver.get("https://www.instagram.com/" + user)
    sleep(2)

    # get the followers and the following lists
    followers = followers_of(driver, user)
    sleep(1)
    following = following_of(driver, user)

    # if the account is private return 0
    if followers == None or following == None:
        return None

    # lists of returned and not returned followers
    returns = []
    not_returns =[]

    # count the returned followers
    returned_following_count = 0
    for follower in followers:
        if follower in following: returns.append(follower)
        else: not_returns.append(follower)

    return returns if returned else not_returns