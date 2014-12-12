@ios
@mobile
Feature: Login to Shield Streams on iOS

    Background: setup the simulator locally with appium
      #Given a "Sauce Labs" iOS Simulator "7.1" running "sauce-storage:vicert_shield_streams.zip"
      Given a "local" ios simulator
        #And I focus the ios simulator
        And I install the BSCA HIT development certificate

    @ios
    @mobile
    Scenario: Invalid credentials (blank) should fail login
        #Given I am an unauthenticated provider user
        When I fail login as a provider with username " " and password " "
        Then I should see "Incorrect username or password"


    @ios
    @mobile
    Scenario: Valid credentials should login successfully
        #Given I am an unauthenticated provider user
        #And I wait for 4 seconds
        When I successfully login as a provider with username "11735" and password "jruffing"
        Then I should see "Critical"



    @ios
    @mobile
    Scenario: Invalid credentials (special characters) should fail login
        #Given I am an unauthenticated provider user
        When I fail login as a provider with username "$admin$admin$admin$admin!@#$%^&&*()" and password "$admin$admin$admin$admin!@#$%^&&*()"
        Then I should see "Incorrect username or password"


    @ios
    @mobile
    Scenario: Invalid credentials (admin/admin) should fail login
        #Given I am an unauthenticated provider user
        When I fail login as a provider with username "admin" and password "admin"
        Then I should see "Incorrect username or password"


