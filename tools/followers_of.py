from time import sleep

# get the followers of a user
def followers_of(driver, user):
   
    # get the user's profile page
    driver.get("https://www.instagram.com/" + user)
    sleep(2)

    # click on the followers link
    try:
        driver.find_element_by_xpath("//a[@href='/" + user + "/followers/']").click()
    except:
        # the account is private
        return None
    sleep(2)

    # get the scrolling box
    scroll_box = driver.find_element_by_xpath("html/body/div[4]/div/div/div[2]")

    # scroll until every follower is loaded
    last_ht, ht = 0, 1
    while last_ht != ht:
        last_ht = ht
        sleep(1)
        ht = driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;", scroll_box)

    # get the followers' names
    links = scroll_box.find_elements_by_tag_name("a")
    names = [name.text for name in links if name.text != ""]
    
    # close follower window
    driver.find_element_by_xpath("html/body/div[4]/div/div/div[1]/div/div[2]/button").click()

    return names