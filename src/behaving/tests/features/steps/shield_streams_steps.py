from behaving.tests.pages.shield_streams_login_page import *
from selenium.common.exceptions import WebDriverException
from behave import given, when, then, step
from behaving.tests.pages.shield_streams_login_page import ShieldStreamsLoginPage
from behaving.tests.pages.shield_streams_critical_stream_page import ShieldStreamsCriticalPage
from subprocess import PIPE

''' Shield Streams Steps
================================================================'''
@step('I successfully login as a provider with username "{user_name}" and password "{pass_word}"')
def successfully_login_as_a_provider(context, user_name, pass_word):
    try:
        critical_screen = ShieldStreamsLoginPage(context).login_as_provider(user_name, pass_word, True)
        wait = WebDriverWait(critical_screen.driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, critical_screen._search_bar_locator)))
        assert True, "Login Succeeded!"
    except TimeoutException as te:
        assert False, te.message
        raise
    except AssertionError as ae:
        assert False, ae.message
        raise
'''
@step('I fail login as a provider with username "{user_name}" and password "{pass_word}"')
def fail_login_as_a_provider(context, user_name, pass_word):
    try:
        sslp = ShieldStreamsLoginPage(context).login_as_provider(user_name, pass_word, False)
        if sslp.is_failed_login_alert_window_displayed() is True:
            assert True, "Login Failed and this was expected. Yay."
        else:
            assert False, "Login Succeeded and this was NOT expected!"
    except AssertionError as ae:
        assert False, ae.message
        raise
'''

@step('I fail login as a provider with username "{user_name}" and password "{pass_word}"')
def fail_login_as_a_provider(context, user_name, pass_word):
    try:
        sslp = ShieldStreamsLoginPage(context)
        sslp.login_as_provider(user_name, pass_word, False)
        if sslp.is_failed_login_alert_window_displayed() is True:
            assert True, "Login Failed and this was expected. Yay."
        else:
            assert False, "Login Succeeded and this was NOT expected!"
    except AssertionError as ae:
        assert False, ae.message
        raise

@step('I focus the ios simulator')
def focus_the_ios_simulator(context):
    ios_sim_focus_cmd = """/bin/sh osascript -e 'tell application "iOS Simulator" activate end tell'"""
    os.system(ios_sim_focus_cmd)

@step('I install the BSCA HIT development certificate')
def install_hit_development_certificate(self):
        try:
            #print "cwd: " + os.getcwd()
            s = subprocess.Popen(['python', 'iosCertTrustManager.py', '-a', 'certs/BSCAShieldStreamsDevelopmentCA.pem'],
                                            shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print "Installing development certificate..."
            while True:
                line = s.stdout.readline()
                if not line:
                    break
                #print line
        except OSError as e:
            raise e


'''
@step('that I am an authenticated provider"')
def create_new_provider_user_and_login_successfully(context, user_name, pass_word):
    try:
        #@TODO Add new user creation via SS API
        # create_user_w_catalyze_or_streams_API()
        sshp = ShieldStreamsLoginPage(context).login_as_provider(user_name, pass_word, False)
        assert sshp.is_failed_login_alert_window_displayed() == False "Login Failed and this was NOT expected!"
    except AssertionError as ae:
        assert False, ae.message
        raise
'''