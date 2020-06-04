from bot import Bot

menu = """
1. Show difference between following and followers 
2. Show top 10 the most active accounts
3. Like photos from hashtag 
4. Exit
"""
username = input("Entry username: ")
password = input("Entry password: ")


def whichAccount():
    choice = input("Do you want check your or other account?(0: My || 1:Other): ")
    if choice == "1":
        b.changeWorkingAccount(input("Entry username: "))
    else:
        pass


b = Bot(username, password)
while True:
    print(menu)
    choice = input("Option (1-4): ")
    if choice == "1":
        whichAccount()
        b.showDiffBtwFollowingAndFollowers()
    elif choice == "2":
        whichAccount()
        b.showActiveUsers()
    elif choice == "3":
        tag = input("Entry name of tag: ")
        how_many = int(input("How many posts to like: "))
        ignore = int(input("Ignore post with more than X likes: "))
        b.likePhotosFromTag(tag, how_many, ignore)
    elif choice == "4":
        exit()
    else:
        continue
