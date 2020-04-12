#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import WebDriverException, NoSuchElementException, NoSuchAttributeException
    from platform import system as os_system
    from time import sleep
    from subprocess import run
    from tempfile import gettempdir
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()
    
def go_to(driver, url, tab_action=False):
    if driver.current_url != 'about:blank':
        wait_until_page_load(driver)
    driver.get(url)

def open_new_tab(driver):
    execute_script(driver, 'window.open(\'\', \'_blank\')')
    window_handle = driver.window_handles[-1]
    switch_to_tab(driver, window_handle)
    return window_handle

def switch_to_tab(driver, window_handle):
    driver.switch_to.window(window_handle)

def close_tab(driver, window_handle=None):
    current_tab = driver.current_window_handle
    driver.switch_to.default_content()
    if window_handle:
        switch_to_tab(driver, window_handle)
    execute_script(driver, 'window.close()')
    if window_handle:
        switch_to_tab(driver, current_tab)
	
def wait_until_page_load(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except WebDriverException:
        pass
        print('Selenium error: Page took too long to be loaded')
        exit()

def wait_until(driver, element, condition='visibility_of_element_located', timeout=15):
    try:
        condition = getattr(EC, condition)
        WebDriverWait(driver, timeout).until(condition((By.CSS_SELECTOR, element)))
    except WebDriverException:
        pass
        print('Selenium error: Element was not presented')
        exit()

def define_ajax_checker(driver, url, js_var='xhr_complete'):
    driver.execute_script('(function(){window.'+js_var+' = false;var oldXHR = window.XMLHttpRequest;function newXHR(){var realXHR = new oldXHR();realXHR.addEventListener("readystatechange", function(){ if(realXHR.responseURL.includes("'+url+'") && realXHR.readyState == 4){'+js_var+' = true;} }, false);return realXHR;}window.XMLHttpRequest = newXHR;})();')
    
def run_ajax_checker(driver, js_var='xhr_complete', timeout=15):
    counter = 0
    while execute_script(driver, 'return typeof('+js_var+') != "undefined" && '+js_var+' == false') and counter < timeout:
        sleep(1)
        counter += 1
    if execute_script(driver, 'return typeof('+js_var+') != "undefined" && '+js_var+' == true') or (execute_script(driver, 'return typeof('+js_var+') == "undefined"') and counter > 0):
        return True
    else:
        return False

def get_element(driver, element, element_order=None):
    wait_until(driver, element)
    element = get_elements(driver, element)[element_order] if element_order else driver.find_element_by_css_selector(element)
    return element

def get_elements(driver, element):
    wait_until(driver, element)
    return driver.find_elements_by_css_selector(element)

def click_element(driver, element, element_order=None):
    wait_until(driver, element, 'element_to_be_clickable')
    el = get_element(driver, element, element_order)
    el.click()

def force_clear_input_element(driver, element, element_order=None):
    element = get_element(driver, element, element_order)
    action_chains = ActionChains(driver)
    action_chains.double_click(element).send_keys(Keys.DELETE).perform()

def type_in_element(driver, element, data, element_order=None, enter=False):
    el = get_element(driver, element, element_order)
    el.clear()
    el.send_keys(data)
    if enter:
        el.send_keys(Keys.ENTER)

def choose_select_option(driver, element, data, element_order=None, by='value'):
    element = get_element(driver, element, element_order)
    select = Select(element)
    if by == 'index':
        select.select_by_index(data)
    elif by == 'text':
        select.select_by_visible_text(data)
    elif by == 'value':
        select.select_by_value(data)
    return select.all_selected_options

def element_exists(driver, element):
    try:
        driver.find_element_by_css_selector(element)
        return True
    except NoSuchElementException:
        pass
        return False

def attribute_exists(element, attribute):
    try:
        element.get_attribute(attribute)
        return True
    except NoSuchAttributeException:
        pass
        return False

def execute_script(driver, code):
    wait_until_page_load(driver)
    return driver.execute_script(code)

def delete_temp_files():
    if os_system().lower() == 'windows':
        temp_dirs = glob(gettempdir() + '/scoped_dir*')
	command = ';'.join(['rd /s /q ' + temp_dir for temp_dir in temp_dirs])
        run(command, shell=True)

def quit(driver=None):
    if driver:
        driver.quit()
    sleep(3)
    delete_temp_files()
    
# EXAMPLE USAGE

try:
    driver = webdriver.Chrome()
    go_to(driver, 'https://www.google.com')
    first_tab = driver.current_window_handle
    type_in_element(driver, '[name=q]', 'facebook', True)
    second_tab = open_new_tab(driver)
    go_to(driver, 'https://www.bing.com')
    type_in_element(driver, '[name=q]', 'facebook', True)
    third_tab = open_new_tab(driver)
    go_to(driver, 'https://www.duckduckgo.com')
    type_in_element(driver, '[name=q]', 'facebook', True)
    switch_to_tab(driver, first_tab)
    sleep(3)
    switch_to_tab(driver, second_tab)
    sleep(3)
    switch_to_tab(driver, third_tab)
    sleep(3)
    close_tab(driver)
    switch_to_tab(driver, second_tab)
    close_tab(driver, first_tab)
    quit(driver)
    print('Automation successfully finished!')
except WebDriverException as e:
    pass
    quit(driver)
    print('Selenium error: ' + str(e).strip('Message: '))
    exit()
