#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def go_to(driver, url):
    if driver.current_url != 'about:blank':
        wait_until_page_load(driver)
    driver.get(url)

def wait_until_page_load(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except WebDriverException:
        pass
        print('Selenium error: Page took too long to be loaded')
        exit()

def wait_until(driver, element, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
    except WebDriverException:
        pass
        print('Selenium error: Element could not be found')
        exit()

def get_element(driver, element):
    wait_until(driver, element)
    return driver.find_element_by_css_selector(element)

def click_element(driver, element):
    el = get_element(driver, element)
    el.click()

def type_in_element(driver, element, data, enter=False):
    el = get_element(driver, element)
    el.clear()
    el.send_keys(data)
    if enter:
        el.send_keys(Keys.ENTER)

def element_exists(driver, element):
    try:
        driver.find_element_by_css_selector(element)
        return True
    except NoSuchElementException:
        pass
        return False

def execute_script(driver, code):
    wait_until_page_load(driver)
    driver.execute_script(code)

def click_alert(driver, ok=True, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
    except WebDriverException:
        pass
        print('Selenium error: No alert was present')
        exit()
    alert = Alert(driver)
    if ok:
        alert.accept()
    else:
        alert.dismiss()
