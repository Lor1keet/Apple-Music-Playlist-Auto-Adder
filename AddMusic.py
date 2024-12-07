from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import os
import time
import json
import pathlib

class AddMusic:
    def __init__(self, account, password, songlist, playlist):
        self.account = account
        self.password = password
        self.songlist = songlist
        self.playlist = playlist
        self.driver = None
        self.wait = None

    def Setup_driver(self):       
        user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "user_data")
        self.options = Options()
        # self.options.add_argument(f"--user-data-dir={user_data_dir}") 
        # self.options.add_argument("--profile-directory=Default")  
    
    def __save_cookie__(self):
        cookies = self.driver.get_cookies()
        json.dump(cookies, open("./cookies.json", "w+"))

    def __load_cookie__(self):
        if os.path.exists("./cookies.json"):
            j = json.load(open("./cookies.json", "r"))
            for d in j:
                self.driver.add_cookie(d)
    
    def __has_login__(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='account-menu-trigger']"))
            )
            return True
        except TimeoutException:
            return False

    def AM_login(self):
        try:
            # 初始化 WebDriver
            self.driver = webdriver.Edge(options=self.options)
            self.driver.get("https://music.apple.com/")
            self.wait = WebDriverWait(self.driver, 20)
            time.sleep(5)
            self.__load_cookie__()
            self.driver.refresh()

            if self.__has_login__():
                return
            
            login_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='sign-in-button']"))
            )
            self.driver.execute_script("arguments[0].click();", login_button)

            iframe = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='ck-container']/iframe"))
            )
            self.driver.switch_to.frame(iframe)

            account_name_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='accountName']"))
            )
            account_name_input.clear()
            account_name_input.send_keys(self.account)

            next_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-test='layout-onboarding-auth-button']"))
            )
            self.driver.execute_script("arguments[0].click();", next_button)

            iframe = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='idms-widget-container']/iframe"))
            )
            self.driver.switch_to.frame(iframe)

            continue_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='continue-password']"))
            )
            self.driver.execute_script("arguments[0].click();", continue_button)

            password_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='password_text_field']"))
            )
            password_input.clear()
            password_input.send_keys(self.password)

            sign_in_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='sign-in']"))
            )
            self.driver.execute_script("arguments[0].click();", sign_in_button)

            self.driver.switch_to.default_content()

            # 等待验证
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='account-menu-trigger']"))
            )

            # time.sleep(20)  
            print("登录成功")
            self.__save_cookie__()
            
        except TimeoutException as e:               
            print(f"登录过程中出现超时: {e}")             
        except Exception as e:               
            print(f"登录失败: {e}")
        

    def SearchAdd(self):
        for song in self.songlist:
            try:
                search_box = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-autocomplete='list']"))
                )
                search_box.clear()
                search_box.send_keys(song)
                search_box.send_keys(Keys.RETURN)

                time.sleep(3)

                more_button = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, 
                    "//div[@data-testid='top-search-lockup-wrapper'][1]//button[@class='contextual-menu__trigger']"))
                )
                self.driver.execute_script("arguments[0].click();", more_button)

                add_to_playlist_button = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//button[@title='添加到歌单']"))
                )
                self.driver.execute_script("arguments[0].click();", add_to_playlist_button)

                target_playlist_button = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//button[@title='{self.playlist}']"))
                )
                self.driver.execute_script("arguments[0].click();", target_playlist_button)
                time.sleep(3)

                print(f"歌曲 '{song}' 已成功添加到歌单 '{self.playlist}'")

            except TimeoutException as e:
                print(f"处理歌曲 '{song}' 时超时: {e}")
            except NoSuchElementException as e:
                print(f"处理歌曲 '{song}' 时找不到元素: {e}")
            except Exception as e:
                print(f"处理歌曲 '{song}' 时发生未知错误: {e}")
                continue

        print("所有歌曲处理完成")