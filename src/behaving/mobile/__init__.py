# Generic setup/teardown for compatibility with pytest et al.
import os
import sys
import httplib
import base64
import atexit
import ConfigParser
import saucelabs.saucerest as saucerest
try:
    import json
except ImportError:
    import simplejson as json


def setup(context, scenario):

    # Setup some defaults b/c something didn't go well
    if not hasattr(context, 'webdriver_url'):
        context.webdriver_url = 'http://127.0.0.1:4723/wd/hub'

    if not hasattr(context, 'ios_caps'):
        context.ios_caps = {
            'platformName': 'iOS',
            'platformVersion': '8.0',
            'language': 'en',
            'deviceName': 'iPhone'
        }

    initialize_webdriver_from_cli_input_config_files_and_or_defaults(context, scenario)

    # ensure we kill the appium server if the tests crash
    def cleanup():
        teardown(context)

    atexit.register(cleanup)


def teardown(context):
    if "sauce" in context.webdriver_url.lower():
        print("Link to your job: https://saucelabs.com/tests/%s" % context.device.session_id)
        #data = json.dumps({ "passed": sys.exc_info() == (None, None, None) })
        data = json.dumps({ "passed": context.scenario.status == "passed"})
        rest = saucerest.SauceRest(
            username=context.sauce_labs_credentials['username'],
            password=context.sauce_labs_credentials['api-key']
        )
        # rest.update_job(self.driver.session_id, data) # broken?
        update_saucelabs(context, context.device.session_id, data)

    # TODO implement custom data field in job @ sauce labs
    #update sauce Results column?
    #data = json.dumps({ "custom-data": context.scenario.GET_THE_EXCEPTION_INFO})
    #update_saucelabs(context, context.device.session_id, data)

    #context.driver.quit() -> redundant from below?

    if hasattr(context, 'device'):
        context.device.quit()
        del context.device




def read(filename):
    '''reads a yaml config file'''
    stream = file(filename, 'r')
    import yaml
    return yaml.load(stream)


def read_sauce_labs_config_and_set_params(context, scenario):
    '''reads the sauce_labs.yaml config file and sets parameters'''

    context.sauce_labs_credentials = read(context._config.saucelabs)

    if not context.sauce_labs_credentials['username']:
        raise 'username must be specified in the sauce labs config file.'

    if context.sauce_labs_credentials['sauce_app_path']:
        context.ios_caps['app'] = context.sauce_labs_credentials['sauce_app_path']
    else:
        raise 'sauce_app_path should be specified in the sauce labs config file.'

    if not context.sauce_labs_credentials['api-key']:
        raise 'no sauce_app_path param provided & no api-key provided in the sauce labs config file. no bueno.'


    context.webdriver_url = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (context.sauce_labs_credentials['username'], context.sauce_labs_credentials['api-key'])

def read_appium_config_and_set_params(context, scenario):
    '''reads the  appium.yaml config file and sets parameters'''

    appium_settings = read(context._config.appium)

    if not appium_settings['xcode_app_path']:
        raise 'xcode_app_path must be specified in the appium config file. typically it can be found @ ~/Library/Developer/Xcode/DerivedData/$APP_NAME-LONG_STRING_W_RANDOM_CHARS/Build/Products/Debug-iphonesimulator/$APP_NAME'

    if not appium_settings['platformName']:
        raise 'platformName must be specified in the appium config file.'

    if not appium_settings['platformVersion']:
        raise 'platformVersion must be specified in the appium config file.'

    if not appium_settings['deviceName']:
        raise 'deviceName must be specified in the appium config file.'

    if not appium_settings['webdriver_url']:
        raise 'webdriver_url must be specified in the appium config file.'

    context.ios_caps = {
        # http://appium.io/slate/en/master/?ruby#appium-server-capabilities
        'platformName': appium_settings['platformName'],
        'platformVersion': appium_settings['platformVersion'],
        'language': 'en',
        'deviceName': appium_settings['deviceName'],
        'appium-version': appium_settings['appium-version'],
        'build': get_application_build_number(context),
        'app': appium_settings['xcode_app_path'],
        'name': scenario.name
        }
    context.local_app_path = appium_settings['xcode_app_path']
    context.webdriver_url = appium_settings['webdriver_url']


def initialize_webdriver_from_cli_input_config_files_and_or_defaults(context, scenario):
    '''checks for appium yaml file from CLI and then checks saucelabs yaml from CLI and sets context'''
    if context._config.appium is None and context._config.saucelabs is None:
        raise 'no appium or saucelabs config file info passed from CLI!'
    elif hasattr(context._config, 'appium') and context._config.appium is not None:
        read_appium_config_and_set_params(context, scenario)
    elif hasattr(context._config, 'saucelabs') and context._config.saucelabs is not None:
        read_sauce_labs_config_and_set_params(context, scenario)


def get_application_build_number(context):
    if hasattr(context._config, 'build'):
        return context._config.build
    elif hasattr(context._config, 'saucelabs'):
        '''pull down zip from sauce and extract and parse'''
        #TODO add some functionality
        return sauce_labs_aut_build_num
    elif hasattr(context._config, 'appium'):
        '''go to xcode path and parse info.plist'''
        #TODO add some functionality
        return local_aut_build_num


def parse_info_plist(local_path_to_app):
    with open(local_path_to_app, 'rb') as fp:
        pl = load(fp)
    print(pl["aKey"])


# saucerest is returning (False, 400, 'Bad request') for some reason
def update_saucelabs(context, jobid, data):
    base64string = base64.encodestring('%s:%s' % (context.sauce_labs_credentials['username'], context.sauce_labs_credentials['api-key']))[:-1]
    connection = httplib.HTTPConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (context.sauce_labs_credentials['username'], jobid),
                    data,
                    headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200