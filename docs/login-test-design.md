# Rokomari Login Automation - Test Design

## 1. Test Scenario

Verify that a valid Rokomari test user can log in successfully using email and password and remains authenticated after page refresh.

## 2. Login Flow

1. Open the Rokomari homepage.
2. Verify the homepage.
3. Verify the Sign In option.
4. Click Sign In.
5. Verify the login page.
6. Enter the valid test email.
7. Click Next.
8. Verify the password field.
9. Enter the valid password.
10. Submit the login form.
11. Verify successful authentication.
12. Verify the authenticated user state.
13. Verify the authentication/session cookie.
14. Refresh the page.
15. Verify the user remains authenticated.
16. Verify the authentication/session cookie still exists.

## 3. Page Object Responsibilities

### HomePage

Responsibilities:

- Open the Rokomari homepage.
- Identify the Sign In option.
- Verify that the Sign In option is visible.
- Click the Sign In option.
- Provide information required to verify the authenticated user state after login.

The HomePage should not:

- Enter login credentials.
- Handle password submission.
- Inspect authentication cookies.
- Contain test-specific pass/fail decisions.

### LoginPage

Responsibilities:

- Verify that the login page is displayed.
- Enter the test user email.
- Click the Next button.
- Verify that the password field appears.
- Enter the test user password.
- Submit the login form.

The LoginPage should not:

- Store hardcoded credentials.
- Decide whether the complete login test passed or failed.
- Handle unrelated homepage actions.
- Inspect authentication/session cookies.

### Test File

The test file will:

- Control the complete login scenario.
- Call the required Page Object methods in the correct order.
- Perform business-level assertions.
- Verify successful authentication.
- Verify authenticated state after refresh.
- Verify authentication/session cookie conditions.

## 4. Locator Design

The automation will prefer stable, user-facing locators instead of DOM-dependent selectors.

| Element | Preferred Locator Strategy |
|---|---|
| Sign In option | Role + accessible name |
| Email field | Label or placeholder |
| Next button | Role + accessible name |
| Password field | Label or placeholder |
| Login/Submit button | Role + accessible name |
| Logged-in user indicator | Role, accessible name, or stable visible text |

Locator priority:

1. Role and accessible name
2. Label
3. Placeholder
4. Stable test-specific attribute
5. Stable visible text
6. CSS selector only when necessary
7. XPath only as a last resort

The final locator for each element will be confirmed during implementation by inspecting the actual Rokomari UI.

Dynamic CSS classes and fragile DOM hierarchy-based selectors should be avoided.

## 5. Action and Method Design

### HomePage

Planned methods:

- `open()`  
  Opens the Rokomari homepage.

- `is_sign_in_visible()`  
  Checks whether the Sign In option is visible.

- `click_sign_in()`  
  Opens the login flow.

- `is_user_logged_in()`  
  Provides the UI state required to verify whether the user is authenticated.

### LoginPage

Planned methods:

- `is_login_page_displayed()`  
  Confirms that the login page is displayed.

- `enter_email(email)`  
  Enters the provided email address.

- `click_next()`  
  Continues from the email step to the password step.

- `is_password_field_visible()`  
  Confirms that the password field is available.

- `enter_password(password)`  
  Enters the provided password.

- `submit_login()`  
  Submits the login form.

### Method Design Principles

- Each method should have one clear responsibility.
- Method names should describe user actions or application state clearly.
- Credentials must be passed into methods instead of being stored inside Page Objects.
- Page Object methods should not contain the complete test flow.
- Page Objects should not contain unrelated business logic.
- Methods should avoid unnecessary waits or duplicated locator logic.

## 6. Assertion Design

The test will perform business-level assertions using the states exposed by the Page Objects.

### Homepage Assertions

The test will verify that:

- The homepage opens successfully.
- The Sign In option is visible before login.

### Login Page Assertions

The test will verify that:

- The login page is displayed after clicking Sign In.
- The password field appears after submitting a valid email.

### Authentication Assertions

After submitting valid credentials, the test will verify that:

- The user is successfully authenticated.
- The expected authenticated page or state is displayed.
- The UI confirms that the user is logged in.

### Session Assertions

The test will verify that:

- An authentication/session-related cookie exists after login.
- The cookie contains a non-empty value.
- The user remains authenticated after page refresh.
- The authentication/session-related cookie still exists after refresh.

### Assertion Principles

- Assertions should be clear and business-readable.
- Important application states should be explicitly verified.
- Page Objects should expose state, while the test decides whether that state is acceptable.
- Assertions should include meaningful failure messages when useful.
- URL validation alone should not be treated as sufficient proof of successful authentication.

## 7. Session and Cookie Handling Design

The authenticated session will be validated using both UI state and browser cookie state.

### Session Validation Flow

After successful login:

1. Verify that the UI shows the user as authenticated.
2. Read browser cookies.
3. Identify the authentication/session-related cookie.
4. Verify that the cookie exists.
5. Verify that the cookie value is not empty.
6. Refresh the page.
7. Verify that the user is still authenticated.
8. Read browser cookies again.
9. Verify that the authentication/session-related cookie still exists.

### Cookie Validation Principles

- The exact cookie name will be confirmed during implementation.
- Full cookie values must never be printed in logs or reports.
- The test will not initially require the cookie value to remain identical after refresh.
- Session persistence will be validated using both UI state and cookie presence.
- Cookie inspection should remain separate from Page Object UI responsibilities.

## 8. Final Test Flow

The automated login scenario will follow this sequence:

1. Open the Rokomari homepage.
2. Verify the Sign In option.
3. Open the login page.
4. Verify the login page.
5. Enter the valid test email.
6. Click Next.
7. Verify the password field.
8. Enter the valid test password.
9. Submit the login form.
10. Verify successful authentication.
11. Verify the logged-in UI state.
12. Verify the authentication/session cookie.
13. Refresh the page.
14. Verify the user remains logged in.
15. Verify the authentication/session cookie still exists.