#!/usr/bin/env python
import shield_streams_login_page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from base import Base


'''Sentimeter Page Object'''
class SentimeterMainPage(object):
    def __init__(self, context):
        self.context = context
        self.driver = context.device
        self._validate_page(self.driver)

    '''locators'''
    _bsc_score_locator = 'bsc_score'
    _calindex_locator = 'calindex_score'
    _titlebar_locator = 'titlebar'
    _influence_meter_locator = 'influence-meter'
    _twitter_expand_locator = 'twitter expand'
    _facebook_expand_locator = 'facebook expand'

    '''page elements'''
    _bsc_score = lambda self: self.driver.find_element_by_id(self._bsc_score_locator)
    _calindex_score = lambda self: self.driver.find_element_by_id(self._calindex_score_locator)
    _titlebar = lambda self: self.driver.find_elements_by_class_name(self._titlebar_locator)
    _influence_meter = lambda self: self.driver.find_elements_by_class_name(self._influence_meter_locator)
    _twitter_expand = lambda self: self.driver.find_elements_by_class_name(self._twitter_expand_locator)
    _facebook_expand = lambda self: self.driver.find_elements_by_class_name(self._facebook_expand_locator)


    def _validate_page(self, _driver):
        # Check to make sure we're on Shield Streams Home Screen
        # Explicitly wait to ensure the element has time to load
        element = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self._bsc_score_locator)))
        if _driver.getTitle() != "Blue Shield Sentimeter":
            raise "This is not the Sentimeter Home Screen!"