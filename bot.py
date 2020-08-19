import random
from re import findall
from time import sleep

from selenium import webdriver
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

    def _likePhoto(self, max):
        self._waitClassName("fr66n")  # wait for fill window by Instagram
        heart = self.driver.find_elements_by_class_name("_8-yf5 ")[5]
        heart_button = self.driver.find_elements_by_class_name("wpO6b")[1]
        likes = findall("\d+", str(self.driver.find_element_by_class_name("EDfFK").text))

        if likes:
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
        """
        self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
        posts = self.driver.find_elements_by_class_name("v1Nh3")[9:]
        posts[0].click()
        self._likePhoto(max)

        i = 0
        while i < limit:
            i += 1 if not self._likePhoto(max) else 0


