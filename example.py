from scraper import Scraper

scraper = Scraper("your_instagram@email.co", "your_instagram_password", chrome_driver_path="C:\your_path\chromedriver.exe")

user = "some_username"
not_returned = scraper.returned_followers(user, False)

users = ["some_username1", "some_username2", "some_username3"]
return_ratios = scraper.returned_followers_ratio(users, max_lists_length=200)

print(not_returned)
print(return_ratios)