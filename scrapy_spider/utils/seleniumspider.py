# -*- coding:utf-8 -*-

from selenium import webdriver


url = 'https://www.baidu.com'

# selenium的基本用法
browser = webdriver.Chrome(executable_path=r'D:\tools\chromedriver_win32\chromedriver.exe')
browser.get(url)
browser.find_element_by_css_selector('xxx').send_keys('xxx')
browser.find_element_by_css_selector('xxx').click()
browser.execute_script('xxx')
html = browser.page_source
print(html)

def no_picture_request():
    chrome_opt = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_opt.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(
            executable_path=r'D:\tools\chromedriver_win32\chromedriver.exe',
            chrome_options=chrome_opt
            )
    browser.get(url)
