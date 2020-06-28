from returned_followers_ratio import ReturnedFollowersRatio

# initialization
rfr = ReturnedFollowersRatio("your_username", "your_password", chrome_driver_path="C:\Program Files (x86)\chromedriver.exe")
# get a user list
users_list = rfr.find_list_from_followers("some_public_great_profile")
# get the returned followers percentage
ratios = rfr.search_list(users_list)
# close the browser
rfr.close()

print("")

print("The final list is:")
for user in ratios:
    print(user["name"] + " --- " + str(user["return_ratio"]))