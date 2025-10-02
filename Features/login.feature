Feature: User Authentication
  As a user
  I want to be able to login to the application
  So that I can access secure features

  Background:
    Given the user is on the login page

  Scenario: Successful login with valid credentials
    When the user enters valid username "Admin"
    And the user enters valid password "admin123"
    And the user clicks the login button
    Then the user should land on the landing page

  @negative
  Scenario Outline: Failed login with invalid credentials
    When the user enters invalid username "<username>"
    And the user enters invalid password "<password>"
    And the user clicks the login button
    Then the user should see error message "<expected_error>"
    And the user should remain on the login page

    Examples:
      | username      | password     | expected_error       |
      |               | secret_sauce | Required             |
      | standard_user |              | Required             |
      | locked_user   | secret_sauce | Invalid credentials  |