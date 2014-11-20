'''#!/usr/bin/env python'''

from behave import configuration
from behave import __main__

# Adding my wanted option to parser.
configuration.parser.add_argument('-u', '--url', help="Address of your url")
configuration.parser.add_argument('-saucelabs', '--saucelabs', help="config file containing sauce labs yaml username and api key")
configuration.parser.add_argument('-appium', '--appium', help="config file for appium settings yaml (used by both appium and saucelabs switches)")
configuration.parser.add_argument('-build', '--build', help="build number to pass as a parameter")
configuration.parser.add_argument('-sauce_app_path', '--sauce_app_path', help="path to the zipped archive containing the iOS simulator .app file")
configuration.parser.add_argument('-capability', '--capability', help='[webdriver] additional capability to set in format "name:value".')

# monkey patch behave
__main__.main()