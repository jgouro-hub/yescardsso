# E2E OIDC Dummy Provider

This project is a **minimal OpenID Connect (OIDC) provider simulator** written in Python using Flask.
It is designed for **end-to-end (E2E) testing** of Salesforce **scratch orgs SSO integration**.
It mimics the main OIDC flows but uses **dummy tokens and user info** for simplicity.

---

## Purpose

- Provide a **mock OIDC Identity Provider** to test Salesforce scratch orgs without requiring a full IdP setup.
- Enable **E2E integration testing** of OAuth 2.0 / OIDC login flows.
- Demonstrate how Salesforce requests tokens and user claims during login.

This service is for **testing only** and is **not suitable for production**.

---

## Features

- **OIDC Discovery**: `/ .well-known/openid-configuration`
- **JWKS endpoint**: `/jwks.json`
- **Authorization Code Flow** (dummy implementation):
  - `/authorize` → user login form.
  - `/login` → issues a dummy authorization code.
  - `/token` → exchanges the code for dummy tokens.
  - `/userinfo` → returns claims for the logged-in user.
- **Testing callback endpoint**: `/callback` for manual inspection.
- **Security guards**:
  - `redirect_uri` must contain **`scratch.my.salesforce.com`**.
  - `email` must end with **`@questel.com`**.

---

## Requirements

- Python 3.9+
- Flask

Install dependencies:

```bash
pip install flask
```

---

## Run

```bash
python app.py
```

The server runs at **http://0.0.0.0:5000**.

---

## Endpoints Documentation

### 1. Discovery Document
```
GET /.well-known/openid-configuration
```
Returns OIDC metadata including endpoints and supported claims.

### 2. JWKS
```
GET /jwks.json
```
Returns a dummy JWKS key set (for testing only).

### 3. Authorize
```
GET /authorize?client_id=test&redirect_uri=https://myorg.scratch.my.salesforce.com/callback&scope=openid%20email&state=12345
```
- Renders a login form with an email field.
- Guard: `redirect_uri` must include `scratch.my.salesforce.com`.

### 4. Login
```
POST /login
```
- Accepts `email`, `redirect_uri`, `state`.
- Redirects back to `redirect_uri` with a dummy `code`.

### 5. Token
```
POST /token
```
Exchanges a dummy code for tokens:
- `access_token`
- `id_token`
- `userinfo`

Guard: `email` must end with `@questel.com`.

### 6. Userinfo
```
GET /userinfo
Authorization: Bearer dummy-access-token-for-user@questel.com
```
Returns the user claims:
```json
{
  "sub": "123456",
  "name": "E2E OIDC User",
  "firstName": "Quality",
  "lastName": "Assurance",
  "email": "user@questel.com",
  "account": "ACME Corp",
  "services": ["EQCORPORATEPLUS"],
  "rights": ["read", "write", "delete"]
}
```

### 7. Callback
```
GET /callback?code=...&state=...
```
Simple endpoint for local browser testing.

---

## Example Flow

1. Start authorization:
```
http://localhost:5000/authorize?client_id=test-client&redirect_uri=https://myorg.scratch.my.salesforce.com/callback&scope=openid%20email&state=12345
```

2. Enter a valid Questel email (e.g., `user@questel.com`).

3. Redirect back to Salesforce scratch org with a code:
```
https://myorg.scratch.my.salesforce.com/callback?code=dummy-code-user@questel.com&state=12345
```

4. Exchange the code for tokens:
```bash
curl -X POST http://localhost:5000/token \
     -d "code=dummy-code-user@questel.com" \
     -d "redirect_uri=https://myorg.scratch.my.salesforce.com/callback" \
     -d "grant_type=authorization_code"
```

5. Call the userinfo endpoint:
```bash
curl -H "Authorization: Bearer dummy-access-token-for-user@questel.com" \
     http://localhost:5000/userinfo
```

---

## Security Guards

- `redirect_uri` → must contain `scratch.my.salesforce.com`.
  Otherwise: **500 error**.
- `email` → must end with `@questel.com`.
  Otherwise: **500 error**.
- No cryptographic signatures → tokens are **dummy strings only**.

---

## Notes

- Use only for **local testing**.
- Tokens are **not signed** and should not be trusted for real authentication.
- Extendable to real JWT signing with `pyjwt` if required.

---
