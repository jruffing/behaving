#!/usr/bin/env python
import shield_streams_critical_stream_page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException

import os
import subprocess

from appium import webdriver

'''
from appium import webdriver
from streams.web.steps import forms
from streams.mobile.steps import find_device_element_by_name_or_id
from base import Base
from selenium.common.exceptions import WebDriverException
'''

import time


'''Shield Streams Login Page Object'''
class ShieldStreamsLoginPage(object):
    def __init__(self, context):
        self.context = context
        self.driver = context.device
        self._validate_page(self.driver)

# region Webdriver Locators


    #Soft Serve App Locators
    _login_button_locator = '//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
    _username_textfield_locator = '//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
    _password_textfield_locator = '//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]'
    #_text_logged_in_from_another_device_locator = '//UIAApplication[1]/UIAWindow[1]/UIAImage[1]/UIAStaticText[2]'
    _login_failed_alert_window_locator = '//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]'
    _login_failed_textfield_locator = 'Incorrect username or password'
    _ios_alert_notifications_locator = '"ShieldStreamsIntegration" Would Like to Send You Notifications'
    _error_alert_window_locator = '//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]'
    _error_text_message_locator = '//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIAStaticText[2]'
    _certificate_missing_locator = "Certificate is missing."


    ''' Vicert/Catalyze App Locators
    _login_button_locator = '//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
    _username_textfield_locator = '//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
    _password_textfield_locator = '//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]'
    _text_logged_in_from_another_device_locator = '//UIAApplication[1]/UIAWindow[1]/UIAImage[1]/UIAStaticText[2]'

    _login_failed_alert_window_locator = '//UIAApplication[1]/UIAWindow[3]/UIAAlert[1]'
    '''

    _login_button = lambda self: self.driver.find_element_by_xpath(self._login_button_locator)
    _username_textfield = lambda self: self.driver.find_element_by_xpath(self._username_textfield_locator)
    _password_textfield = lambda self: self.driver.find_element_by_xpath(self._password_textfield_locator)
    _logged_in_user_textfield = lambda self: self.driver.find_element_by_xpath(self._text_logged_in_from_another_device_locator)

    _login_failed_alert_window = lambda self: self.driver.find_element_by_xpath(self._login_failed_alert_window_locator)
    _error_alert_window = lambda self: self.driver.find_element_by_xpath(self._error_alert_window_locator)
    _error_text_message = lambda self: self.driver.find_element_by_xpath(self._login_failed_alert_locator)
    _ios_alert_notifications = lambda self: self.driver.find_element_by_name(self._ios_alert_notifications_locator)
    _certificate_missing = lambda self: self.driver.find_element_by_name(self._certificate_missing_locator)
    _login_failed_textfield = lambda self: self.driver.find_element_by_name(self._login_failed_textfield_locator)
    #streams_navigation_bar              = lambda self: self.webdriver.find_element_by_xpath(self.streams_navigation_bar_locator)
    # Page objects all override the _validate_page() method so pages
    # can self validate upon creation.
# endregion



    def _validate_page(self, driver):
        # Check to make sure we're on Shield Streams Login screen
        # Explicitly wait to ensure the element has time to load
        if self.is_error_alert_window_displayed() is True:
            self.clear_alert_window()
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, self._login_button_locator)))
        if driver.find_element_by_xpath(self._username_textfield_locator).get_attribute('value') != "Username":
            raise "This is not the Shield Streams Login Screen."

    # Here we are implementing the validate result contains method.
    def result_contains(self, text_to_check):
        "Simple check to see if the word occurs in the page."
        return text_to_check in self.driver.page_source

    def login_as_provider(self, user_name, pass_word, expected_successful_login=True):
        """Login to the application

        :Args:
        - user_name - the username of the credentials
        - pass_word - the password of the credentials
        - expected_successful_login - Boolean:
            True = expecting the login to succeed
            False = expecting the login to fail

        :Usage:
            login_as_provider(doc@tor.com, my_GOOD_secret_password, True)
            login_as_provider(doc@tor.com, my_BAD_secret_password, False)

        :Returns:
            a page object
        """

        self._login(user_name, pass_word)

        ''' # this is the certificate missing crap that I hopefully don't need after adding the certificate
        # installation in the background of each feature
        # check that developer certificate is not missing and install it if missing
        if self.is_development_certificate_missing() is True:
            self.install_development_certificate()
            # we need to login a 2nd time
            self._login(user_name, pass_word)
            if self.is_development_certificate_missing() is True:
                raise Exception("Something went wrong and the development certificate did not install")
        '''
        # return a page object
        if expected_successful_login is True:
            return shield_streams_critical_stream_page.ShieldStreamsCriticalPage(self.context)
        elif expected_successful_login is False:
            return self
        else:
            raise

    def enter_username(self, user_name):
        """Input Username into the textfield"""
        self._username_textfield().click()
        self._username_textfield().set_value(user_name)
        try:
            assert self._username_textfield().get_attribute('value') == user_name, \
                "Username input error: " + user_name + " != " + self._username_textfield().get_attribute('value')
        except AssertionError as ae:
            assert False, ae.message
            raise

    def enter_password(self, pass_word):
        """Enter Password into the textfield"""
        self._password_textfield().click()
        self._password_textfield().set_value(pass_word)
        try:
            '''iOS limits ability to check secure textfield text, can only check length'''
            assert len(self._password_textfield().get_attribute('value')) == len(pass_word), \
                "Password Input error: the input password length doesn't match " \
                + self._password_textfield_locator + " password length"
        except AssertionError as ae:
            assert False, ae.message
            raise

    def hide_keyboard(self):
        self.driver.hide_keyboard('Next') #-> Not working with Appium-Python-Client...bug?
        #self.driver.find_element_by_name("Next").click()

    def tap_login_button(self):
        """Login to the application"""
        self._login_button().click()

    def _login(self, user_name, pass_word):
        """Login to the application"""
        self.enter_username(user_name)
        self.enter_password(pass_word)
        try:
            self.driver.find_element_by_name("Return").click() # press "return" key
        except NoSuchElementException:
            raise

    def is_user_logged_in(self):
        """Check if user is authenticated"""
        #TODO(jay) move this to base page object
        #TODO(jay) update logic to check for presence of logout button
        pass

    def did_we_get_kicked_out(self):
        if self.driver.find_element_by_xpath(self._text_logged_in_from_another_device_locator).get_attribute(
                'value') == "You have logged in from another device.":
            return True
        else:
            return False

    def is_failed_login_alert_window_displayed(self):
        """Check for Failed Login Alert window

        :Args:
            none

        :Usage:
            is_failed_login_alert_window_displayed()

        :Returns:
            boolean
                True: The Failed Login Alert Window is displayed
                False: The Failed Login Alert Window is NOT displayed
        """
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present(), 'Timed out waiting for failed login alert')
            #wait = WebDriverWait(self.driver, 5)
            #element = wait.until(EC.presence_of_element_located((By.NAME, self._login_failed_textfield)))
            return True
        except TimeoutException:
                print "login failed alert was not found"
                return False

    def is_error_alert_window_displayed(self, action_on_all_alerts=None):
        """Checks for presence of an alert window

        :Args:
            action_on_all_alerts
                dismiss: dismiss the alerts (click cancel button if present)
                accept: accept the alerts (click OK button if present)

        :Usage:
            self.is_failed_login_alert_window_displayed()
            self.is_failed_login_alert_window_displayed("dismiss")
            self.is_failed_login_alert_window_displayed("accept")

        :Returns:
            boolean
                True: an alert window is displayed
                False: an alert window is displayed
            *if you set action_on_all_alerts=accept or =dismiss the action will be attempted, default is to take no action
        """
        found_alert = False

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for alerts')
            alert = self.driver.find_element_by_class_name('UIAAlert') # test for alert present
            if len(alert.text) > 0:
                found_alert = True
                print "found alert: " + alert.text
                if action_on_all_alerts == "dismiss":
                    self.driver.switch_to_alert()
                    alert.dismiss()
                    return True
                elif action_on_all_alerts == "accept":
                    self.driver.switch_to_alert()
                    alert.accept()
                    return True
                else:
                    return True
            else:
                return False
        except TimeoutException:
                print "no development certificate alerts found"
                return False
        except NoAlertPresentException:
                print "no development certificate alerts found"
                return False
        except NoSuchElementException:
                print "no development certificate alerts found"
                return False

    def clear_alert_window(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for alerts')
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            alert.accept()
            print "alert accepted: " + alert_text
        except TimeoutException:
            print "no (more) alerts found"
        except NoAlertPresentException:
            print "no (more) alerts found"

    def clear_alert_windows(self):
        #alert = self.find_element_by_class_name('UIAAlert') # test for alert present
        while True:
            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for alerts')
                alert = self.driver.switch_to_alert()
                alert_text = alert.text
                alert.accept()
                print "alert accepted: " + alert_text
            except TimeoutException:
                print "no (more) alerts found"
            except NoAlertPresentException:
                print "no (more) alerts found"


    def is_development_certificate_missing(self):
        try:
            print "checking for certificate is missing alert..."
            WebDriverWait(self.driver, 10).until(EC.alert_is_present(), 'Timed out waiting for cert missing alert')
            #wait = WebDriverWait(self.driver, 10)
            #wait.until(EC.presence_of_element_located((By.NAME, self._certificate_missing_locator)), 'no development certificate alerts found, cert is likely installed')
            print "certificate is missing alert prompt found"
            cert_missing = self.driver.switch_to_alert()
            cert_missing.accept()
            print "cert missing alert prompt was accepted"
            return True
        except TimeoutException:
            print "timed out - no development certificate alert was found"
            return False
        except NoAlertPresentException:
            print "not present - no development certificate alert was found"
            return False
        except NoSuchElementException:
            print "nosuchelement - no development certificate alert was found"
            return False
        else:
            return False


    def install_development_certificate(self):
        try:
            print "cwd: " + os.getcwd()
            s = subprocess.Popen(['python', '/streams_ui_test/iosCertTrustManager.py', '-a', '/streams_ui_test/certs/BSCAShieldStreamsDevelopmentCA.pem'],
                                            shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                line = s.stdout.readline()
                if not line:
                    break
                #logging.info(line)
                print line
        except OSError as e:
            raise e