import random
from re import findall
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Bot:

    def __init__(self, username, password):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome()
        self.driver.delete_all_cookies()
        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        self.wait = WebDriverWait(self.driver, 5)
        self.username = username
        self.login(self.username, password)
        self._waitThenClickXPATH('//*[@id="react-root"]/section/main/div/div/div/div/button')
        self._waitThenClickXPATH("//button[@class='aOOlW   HoLwm ']")  # click button to hide notification window

    def __del__(self):
        self.driver.close()

    def changeWorkingAccount(self, name):
        self.username = name

    def _waitThenClickXPATH(self, path):
        self.wait.until(EC.presence_of_element_located((By.XPATH, path)))
        self.driver.find_element_by_xpath(path).click()

    def _waitXPATH(self, path):
        self.wait.until(EC.presence_of_element_located((By.XPATH, path)))

    def _waitClassName(self, name):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, name)))

    def login(self, username, password):
        self._waitXPATH("//input[@name='username']")

        username_i = self.driver.find_element_by_xpath("//input[@name='username']")
        username_i.send_keys(username)
        self.username = username

        password_i = self.driver.find_element_by_xpath("//input[@name='password']")
        password_i.send_keys(password)

        self._waitThenClickXPATH("//button[@type='submit']")

    def _getUserNamesFromPopUpWindow(self, limit):
        while len(self.driver.find_elements_by_class_name('RR-M- ')) < limit:
            self.driver.execute_script("""
            e = document.getElementsByClassName("isgrP")[0];
            e.scrollTop = e.scrollHeight;
            """)
            sleep(0.5)

        links = self.driver.find_elements_by_xpath(
            "//a[@class='FPmhX notranslate  _0imsa ']")  # get user nick from link

        names = [link.text for link in links]
        self._waitThenClickXPATH("/html/body/div[4]/div/div[1]/div/div[2]/button")  # close pop-up window

        return names

    def _getUserNamesFromLikeWindow(self, popup):
        likes = self.driver.find_elements_by_class_name('HVWg4')
        while len(likes) == 0:
            popup.click()
            sleep(1)
            likes = self.driver.find_elements_by_class_name('HVWg4')

        accounts = []

        while True:
            accounts += [str(like.text).split("\n")[0] for like in likes]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", likes[-1])
            self._waitClassName('HVWg4')

            last = likes[-1]
            sleep(0.7)
            likes = self.driver.find_elements_by_class_name('HVWg4')
            if last == likes[-1]:
                sleep(1)
                last = likes[-1]
                likes = self.driver.find_elements_by_class_name('HVWg4')
                if last == likes[-1]:
                    break

        self._waitThenClickXPATH("/html/body/div[5]/div/div[1]/div/div[2]/button")
        return set(accounts)

    def showDiffBtwFollowingAndFollowers(self):
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        # get number of followers
        number_of_followers = int(str(
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text).replace(" ", ""))

        # get number of following
        number_of_following = int(
            self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text)

        # get list of followers
        self.driver.find_element_by_xpath("//a[@href='/{}/followers/']".format(self.username)).click()
        sleep(1)
        followers = self._getUserNamesFromPopUpWindow(number_of_followers)

        # get list of following
        self.driver.find_element_by_xpath("//a[@href='/{}/following/']".format(self.username)).click()
        sleep(1)
        following = self._getUserNamesFromPopUpWindow(number_of_following)

        not_following_back = [follow for follow in following if follow not in followers]

        print(not_following_back)

    def _likePhoto(self, max):
        self._waitClassName("fr66n")  # wait for fill window by Instagram
        heart = self.driver.find_elements_by_class_name("_8-yf5 ")[4]
        heart_button = self.driver.find_elements_by_class_name("wpO6b")[0]
        likes = findall("\d+", str(self.driver.find_element_by_class_name("EDfFK").text))

        if len(likes) != 0:
            likes = max if len(likes) > 1 else int(likes[0])
        else:
            likes = 0

        if heart.get_attribute(
                "fill") != "#ed4956" and likes < max:  # if photo hasn't liked yet and number of likes is less than max
            heart_button.click()
            sleep(random.randint(1, 4))
            self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            return 0

        self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        return 1

    def likePhotosFromTag(self, tag, limit=60, max=30):
        """
        Like photo from tag if post meet the requirements
        :param tag: name of tag
        :param limit: maximum number of likes
        :param max: ignore post with more than N likes
        :return:
        """
        self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
        posts = self.driver.find_elements_by_class_name("v1Nh3")[9:]
        posts[0].click()
        self._likePhoto(max)

        i = 0
        while i < limit:
            i += 1 if not self._likePhoto(max) else 0

    @staticmethod
    def _getOfNumberLikesFromUser(accounts, account_likes):
        for account in accounts:
            if account in account_likes.keys():
                account_likes[account] += 1
            else:
                account_likes[account] = 1
        return account_likes

    def showActiveUsers(self):
        account_likes = {}
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        self.driver.find_elements_by_class_name("v1Nh3")[0].click()
        while True:
            self._waitClassName("fr66n")  # wait for fill window by Instagram
            likes = self.driver.find_elements_by_class_name("yWX7d")[2]

            accounts = self._getUserNamesFromLikeWindow(likes)
            account_likes = self._getOfNumberLikesFromUser(accounts, account_likes)

            try:
                self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()  # check next post
            except NoSuchElementException:  # if reach end break loop
                break

        account_likes = sorted(account_likes.items(), key=lambda x: x[1], reverse=True)
        for i, (account, likes) in enumerate(account_likes):
            print(f"{i + 1}. {account} {likes} likes")
            if i > 9:
                break
