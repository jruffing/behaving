#!/usr/bin/env python
import shield_streams_login_page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from appium import webdriver
from base import Base


'''Shield Streams Critical Page Object'''
class ShieldStreamsCriticalPage(object):
    def __init__(self, context):
        self.context = context
        self.driver = context.device
        self._validate_page(self.driver)

    _incoming_streams_table_locator = '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]'
    _nav_bar_title_statictext_locator = '//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAStaticText[1]'
    _search_bar_locator = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIATableView[1]/UIASearchBar[1]'

    _nav_bar = lambda self: self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]')
    _search_bar = lambda self: self.driver.find_element_by_xpath(self._search_bar_locator)
    ''' # from vicert app
    _nav_bar_back_button = lambda self: self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]')
    _flagged_messages_count = lambda self: self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIAStaticText[2]')
    _flagged_streams_ = lambda self: self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIAStaticText[2]')        _nav_bar_title_statictext = lambda self: self.driver.find_element_by_xpath(self._nav_bar_title_locator)
    '''
    # Page objects all override the _validate_page() method so pages
    # can self validate upon creation.

    def _validate_page(self, _driver):
        # Check to make sure we're on Shield Streams Home Screen
        # Explicitly wait to ensure the element has time to load
        element = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.XPATH, self._nav_bar_title_statictext_locator)))
        if _driver.find_element_by_xpath(self._nav_bar_title_statictext_locator).get_attribute('value') != "Critical":
            raise "This is not the Critical Streams Screen!"

    def search(self, search_term):
        """Input text to search"""
        self._search_bar().click()
        self._search_bar().set_value(search_term)
        try:
            assert self._search_bar().get_attribute('value') == search_term, \
                "Search term input error: " + search_term + " != " + self._search_bar().get_attribute('value')
        except AssertionError as ae:
            assert False, ae.message
            raise
        try:
            self.driver.find_element_by_name("Search").click() # press "Search" key
        except NoSuchElementException as nsee:
            assert False, nsee.message
            raise


class StreamsCategoriesTableGroup():
    """Table containing the Shield Streams Categories"""
    def __init__(self, driver):
        """
        :type driver: webdriver
        """
        self._driver = driver

    _incoming_streams_table_locator = '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]'
    _incoming_streams_Flagged_category_locator = '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]'
    _incoming_streams_Refill_Request_category_locator = '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]'
    _incoming_streams_Admission_category_locator = '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]'

    _incoming_streams_table = lambda self: self._driver.find_element_by_xpath(self._incoming_streams_table_locator)
    #_incoming_streams_Flagged_row =