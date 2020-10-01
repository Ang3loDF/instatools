from time import sleep
from tools.followers_of import followers_of
from tools.following_of import following_of

def returned_followers_ratio(driver, users, max_lists_length=400):
    return search_list(driver, users, max_lists_length)

# launch the searching process. Find the percentage of returned follower for every user in the
# list and sort them from highest to lowest
def search_list(driver, user_list, max_lists_length):
    
    # define the list
    users_ratios = [None] * len(user_list)

    print("Scanning the users of the list...")

    # for every user compare the followers to following and add to the list
    for i in range(len(user_list)):
        print("User " + str(i) + " of " + str(len(user_list)) + " scanning - " + user_list[i])
        ratio = search_user(driver, user_list[i], max_lists_length)
        users_ratios[i] = {"name": user_list[i], "return_ratio": ratio}

    # sorting function - for every user get the return_ratio value
    def sortingKey(e):
        return e["return_ratio"]

    # sort from the highest with the sorting function
    users_ratios.sort(key=sortingKey, reverse=True)

    return users_ratios


# find the percentage of returned follower for a single user
def search_user(driver, user, max_lists_length):
    
    # get the user's profile page
    driver.get("https://www.instagram.com/" + user)
    sleep(2)

    # if has too much followers/following return -1
    if (not is_followers_list_short(driver, user, max_lists_length)) or (not is_following_list_short(driver, user, max_lists_length)):
        return -1.0

    # get the followers and the following lists
    followers = followers_of(driver, user)
    sleep(1)
    following = following_of(driver, user)

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


# check if the followers number is small enough 
def is_followers_list_short(driver, user, max_lists_length):
    
    # get the number of followers
    try:
        # if the account is not private
        followers_num_str = driver.find_element_by_xpath("//a[@href='/" + user + "/followers/']/span").text.replace(".", "")
    except: 
        # if the account is private
        followers_num_str = driver.find_element_by_xpath("html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span").text.replace(".", "")
    
    # convert the number of followers to int
    try:
        followers_num = int(followers_num_str)
    except:
        return False

    # check the number of follower is smaller than the max list length
    if followers_num > max_lists_length:
        return False
    return True



# check if the following number is small enough 
def is_following_list_short(driver, user, max_lists_length):

    # get the number of following
    try:
        # if the account is not private
        following_num_str = driver.find_element_by_xpath("//a[@href='/" + user + "/following/']/span").text.replace(".", "")
    except:
        # if the account is private
        following_num_str = driver.find_element_by_xpath("html/body/div[1]/section/main/div/header/section/ul/li[3]/span/span").text.replace(".", "")
    
    # convert the number of following to int
    try:
        following_num = int(following_num_str)
    except:
        return False
    
    # check the number of following is smaller than the max list length
    if following_num > max_lists_length:
        return False
    return True