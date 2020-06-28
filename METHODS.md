# Methods

## ReturnedFollowerRatio() - Class Constructor
Initialize the process with the correct values. Open the browser and log you into Instagram.
#### Parameters
* username = "" - username (or email) of your Instagram account
* psw = "" - password of your Instagram account
* chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe" - the directory path of your Chrome Web Driver
* max_lists_length = 400 - the max number of followers/following that a profile can have to be scanned, if it exceeds, it will be ignored. It is important to set a value that your machine can support.

#### Example
```
rfr = ReturnedFollowersRatio("my_great_account", "my_secret_psw", chrome_driver_path="C:\my_dir\chromedriver.exe")
```

## find_list_from_followers()
If you don't have a list of users to search for the best users to follow, you can use this method that gets a list of users from the followers of a specified profile.
#### Parameters
* user = "" - the username of the user from which you want to take the list

#### Return
Array of string with the username of the users.
#### Example
```
user_list = rfr.find_list_from_followers("amazing_profile")
```

## search_list()
Calculate the percentage of returned followers for all the users in the list.
#### Parameters
* user_list = [] - array of string containing the username of the users to scan

#### Return
An array of dictionaries (sorted from highest to lowest) containing:
* name - the username of the user
* return_ratio - the percentage of returned followers. Normally a value from 0 to 1, 0 if the user is private, -1 if the user exceeds the maximum number of followers/following.

#### Example
```
ratios = rfr.search_list(users_list)
for user in ratios:
    print(user["name"] + " --- " + str(user["return_ratio"]))
```

## search_user()
Calculate the percentage of returned followers for a single user.
#### Parameters
* user = "" - username of the user to scan

#### Return
The percentage of returned followers. Normally a value from 0 to 1, 0 if the user is private, -1 if the user exceeds the maximum number of followers/following.
#### Example
```
ratio = rfr.search_user("amazing_user")
print(ratio)
```

## close()
Close the browser. No parameters, no return
#### Example
```
rfr.close()
```