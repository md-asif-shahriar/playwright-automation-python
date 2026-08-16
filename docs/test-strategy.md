# Rokomari Login Automation - Test Strategy

## 1. Feature Under Test

Rokomari User Login / Authentication

## 2. Objective

The objective of this automation is to verify that a valid Rokomari test user can successfully log in using email and password and that the authenticated session remains active after refreshing the browser.

## 3. In Scope

The following validations are included in the initial automation scope:

- Open the Rokomari homepage.
- Verify that the homepage loads successfully.
- Verify that the Sign In option is available.
- Click the Sign In option.
- Verify navigation to the login page.
- Verify the login page is displayed correctly.
- Enter a valid test account email.
- Click the Next button.
- Verify that the password field appears.
- Enter a valid password.
- Submit the login form.
- Verify successful login.
- Verify navigation to the expected page after login.
- Verify that the user is shown as logged in.
- Verify that an authentication/session-related cookie exists after login.
- Refresh the page.
- Verify that the user remains logged in after refresh.
- Verify that the authentication/session cookie still exists after refresh.

## 4. Out of Scope

The following scenarios are not included in the initial phase:

- Invalid email
- Invalid password
- Empty email/password
- OTP login
- Social login
- Registration
- Forgot password
- Logout
- Account lockout
- CAPTCHA handling
- Cart
- Checkout
- Payment
- Search
- API testing
- Performance testing
- Security testing
- Mobile/responsive testing
- Cross-browser testing

## 5. Test Scenario

### Scenario: Successful login with valid email and password

**Preconditions:**
- Rokomari website is accessible.
- A dedicated valid Rokomari test account is available.
- The test account is active and not locked.
- Valid login credentials are available securely.

**Test Steps:**
1. Open the Rokomari homepage.
2. Verify that the homepage loads successfully.
3. Verify that the Sign In option is visible.
4. Click the Sign In option.
5. Verify that the login page is displayed.
6. Enter a valid email address.
7. Click the Next button.
8. Verify that the password field appears.
9. Enter the valid password.
10. Submit the login form.
11. Verify that login is successful.
12. Verify that the expected authenticated page is displayed.
13. Verify that the user appears as logged in.
14. Verify that an authentication/session-related cookie exists.
15. Refresh the page.
16. Verify that the user remains logged in.
17. Verify that the authentication/session-related cookie still exists.

## 6. Acceptance Criteria

The test will be considered passed only if all of the following conditions are satisfied:

- The homepage loads successfully.
- The Sign In option is visible and usable.
- The login page opens successfully.
- The email can be entered.
- The Next button proceeds to the password step.
- The password field becomes available.
- Valid credentials result in successful authentication.
- The expected authenticated page is displayed after login.
- The UI confirms that the user is logged in.
- An authentication/session-related cookie exists after login.
- The user remains authenticated after refreshing the page.
- The authentication/session-related cookie still exists after refresh.

If any required validation fails, the test will be considered failed.

## 7. Test Data Strategy

- A dedicated Rokomari test account will be used for automation.
- The test account must remain active and usable.
- The account should not be used for destructive or risky test activities.
- Test credentials must not be hardcoded in test files.
- Test credentials must not be committed to GitHub.
- Local execution will use environment variables for credentials.
- CI execution will use GitHub Actions Secrets.
- Sensitive data such as passwords, authentication tokens, or session cookie values must not be printed in logs or reports.

## 8. Credential Handling

The automation will use the following logical credential variables:

- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`

For local execution, these values will come from environment variables or a local environment configuration file that is excluded from Git.

For GitHub Actions, the same credentials will be stored securely as repository secrets.

The framework must never:

- Hardcode credentials inside test files.
- Commit credentials to Git.
- Print passwords in logs.
- Print full authentication/session cookie values.
- Store sensitive authentication files in the repository.

## 9. Locator Strategy

The automation will use stable and user-facing Playwright locators whenever possible.

Locator preference:

1. Role and accessible name
2. Label
3. Placeholder
4. Stable test-specific attribute, if available
5. Stable text
6. CSS selector only when necessary
7. XPath only as a last option

The framework should avoid:

- Long or complex XPath expressions.
- Locators based on dynamic CSS classes.
- Fragile DOM hierarchy-based selectors.
- Duplicate locators across multiple test files.
- Fixed waits used to compensate for unstable locators.

Reusable page locators and interactions will be maintained inside the appropriate Page Object or component.

## 10. Session and Cookie Validation Strategy

After successful login, the automation will verify that the authenticated session has been created successfully.

The test will:

- Confirm that the user is authenticated through the UI.
- Inspect browser cookies after successful login.
- Identify the cookie or cookies related to the authenticated session.
- Verify that the expected authentication/session cookie exists.
- Verify that the cookie contains a non-empty value.
- Refresh the page.
- Verify that the user remains authenticated after refresh.
- Verify that the authentication/session cookie is still available after refresh.

The test will not initially require the cookie value before and after refresh to be identical.

The exact authentication/session cookie name will be confirmed through browser inspection before implementing the final assertion.

Full session cookie values must not be printed in logs or reports.

## 11. Risks and Flakiness Prevention

Since Rokomari is an external production website, the automation may be affected by conditions outside our control.

Possible risks include:

- Slow or unstable internet connection.
- Temporary website downtime.
- Changes in the Rokomari UI or login flow.
- Dynamic elements or delayed page loading.
- CAPTCHA or additional security verification.
- Test account lockout or authentication changes.
- Session or cookie behavior changing over time.
- Third-party services affecting page loading.

To reduce flakiness, the framework will:

- Use Playwright's built-in auto-waiting.
- Avoid fixed waits such as `time.sleep()`.
- Use stable and meaningful locators.
- Use explicit assertions for expected application states.
- Keep each test independent.
- Avoid unnecessary retries.
- Capture useful failure diagnostics such as screenshots, logs, and traces.
- Keep test data and authentication setup controlled.
- Avoid destructive actions on the production website.

## 12. Definition of Done

Module 1 will be considered complete when:

- The login automation objective is clearly defined.
- In-scope and out-of-scope areas are documented.
- The successful login test scenario is documented.
- Acceptance criteria are defined.
- Test data and credential handling strategies are defined.
- Locator strategy is documented.
- Session and cookie validation strategy is documented.
- Major automation risks are identified.
- Flakiness prevention principles are documented.
- No sensitive credentials or session values are stored in the repository.
- The test strategy document has been reviewed and is ready to guide framework implementation.