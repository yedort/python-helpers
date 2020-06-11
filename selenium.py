#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import WebDriverException, NoSuchElementException, NoSuchAttributeException
    from time import sleep
    from yedorthelpers import YedortHelpers as helpers
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()

class YedortSelenium(webdriver.Chrome):
    def __init__(self, headless=False, maximize_window=False, *args):
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        if maximize_window:
            options.add_argument('--start-maximized')
        super().__init__(*args, options=options)
        self.driver = super()

    def go_to(self, url):
        self.driver.switch_to.default_content()
        if self.driver.current_url != 'about:blank':
            self.wait_until_page_load()
        self.driver.get(url)

    def open_new_tab(self):
        self.run_javascript('window.open(\'\', \'_blank\')')
        window_handle = self.driver.window_handles[-1]
        self.switch_to_tab(window_handle)
        return window_handle

    def get_tab(self, tab):
        if isinstance(tab, int):
            if tab <= len(self.driver.window_handles):
                tab = self.driver.window_handles[tab - 1]
            else:
                raise WebDriverException('Tab index was out of range.')
        return tab

    def switch_to_tab(self, tab):
        tab = self.get_tab(tab)
        self.driver.switch_to.window(tab)

    def close_tab(self, tab=None):
        tab = self.get_tab(tab)
        current_tab = self.driver.current_window_handle
        if tab is current_tab:
            tab = None
        self.driver.switch_to.default_content()
        if tab:
            self.switch_to_tab(tab)
        self.driver.close()
        previous_tab = current_tab if tab else self.driver.window_handles[0]
        self.switch_to_tab(previous_tab)
        
    def wait_until_page_load(self, timeout=15):
        try:
            driver_ins = self.driver
            WebDriverWait(self.driver, timeout).until(lambda driver_ins: driver_ins.execute_script('return document.readyState') == 'complete')
        except WebDriverException:
            pass
            print('Selenium error: Page took too long to be loaded')
            exit()

    def wait_until(self, element, condition=None, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
            if condition:
                condition = getattr(EC, condition)
                WebDriverWait(self.driver, timeout).until(condition((By.CSS_SELECTOR, element)))
        except WebDriverException:
            pass
            print('Selenium error: Element "' + element + '" was not presented')
            exit()

    def set_ajax_checker(self, url, js_var='xhr_complete'):
        self.run_javascript('(function(){window.'+js_var+' = false;var oldXHR = window.XMLHttpRequest;function newXHR(){var realXHR = new oldXHR();realXHR.addEventListener("readystatechange", function(){ if(realXHR.responseURL.includes("'+url+'") && realXHR.readyState == 4){'+js_var+' = true;} }, false);return realXHR;}window.XMLHttpRequest = newXHR;})();')
        
    def run_ajax_checker(self, js_var='xhr_complete', timeout=15):
        counter = 0
        while self.run_javascript('return typeof('+js_var+') != "undefined" && '+js_var+' == false') and counter < timeout:
            sleep(1)
            counter += 1

    def switch_to_frame(self, element, element_order=None):
        element = self.get_element(element, element_order)
        self.driver.switch_to.frame(element)

    def get_element(self, element, element_order=None):
        self.wait_until(element)
        element = self.get_elements(element)[element_order] if element_order else self.driver.find_element_by_css_selector(element)
        return element

    def get_elements(self, element):
        self.wait_until(element)
        return self.driver.find_elements_by_css_selector(element)

    def click_element(self, element, element_order=None):
        self.wait_until(element, 'element_to_be_clickable')
        el = self.get_element(element, element_order)
        el.click()

    def make_element_visible(self, element):
        element = element.replace('\'', '\\\'')
        self.run_javascript('var elements = document.querySelectorAll(\'' + element + '\');for(var i = 0;i < elements.length;i++){var element = elements[i];element.style.visibility = \'visible\';element.style.height = \'1px\';element.style.width = \'1px\';element.style.opacity = \'1\';}')

    def clear_input_element(self, element, element_order=None):
        element = self.get_element(element, element_order)
        action_chains = ActionChains(driver)
        action_chains.double_click(element).send_keys(Keys.DELETE).perform()

    def type_in_element(self, element, data, element_order=None, enter=False):
        el = self.get_element(element, element_order)
        el.clear()
        el.send_keys(data)
        if enter:
            el.send_keys(Keys.ENTER)

    def choose_select_option(self, element, data, element_order=None, by='value'):
        element = self.get_element(element, element_order)
        select = Select(element)
        if by == 'index':
            select.select_by_index(data)
        elif by == 'text':
            select.select_by_visible_text(data)
        elif by == 'value':
            select.select_by_value(data)
        return select.all_selected_options

    def element_exists(self, element):
        try:
            self.driver.find_element_by_css_selector(element)
            return True
        except NoSuchElementException:
            pass
            return False

    def attribute_exists(self, element, attribute):
        try:
            element.get_attribute(attribute)
            return True
        except NoSuchAttributeException:
            pass
            return False

    def run_javascript(self, code):
        self.wait_until_page_load()
        return self.driver.execute_script(code)

    def quit(self):
        self.driver.quit()
        sleep(3)
        helpers.delete_temp_files('scoped_dir*')
