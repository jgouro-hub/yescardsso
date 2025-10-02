# Yes-Card SSO (Dummy OIDC Server)

A minimal **dummy Single Sign-On (SSO) server** written in Python 3 using Flask.
It acts like an **OpenID Connect provider** but always approves authentication (the “yes-card” concept).
Useful for **testing integration flows** without requiring a real IdP like Keycloak, Okta, or Azure AD.

---

## ✨ Features
- OpenID Connect-style endpoints:
  - `/.well-known/openid-configuration`
  - `/authorize`
  - `/token`
  - `/userinfo`
  - `/jwks.json`
- Always returns a successful login and static tokens.
- Dummy user info (`yescard@example.com`) for consistent tests.
- Perfect for development and CI environments.

---

## 📦 Requirements
- Python **3.8+**
- Dependencies listed in `requirements.txt`:
  ```txt
  flask>=2.3
  pyjwt>=2.9   # optional, for JWT support if needed
  ```

---

## 🚀 Setup & Run

### 1. Clone the project
```bash
git clone https://github.com/your-org/yes-card-sso.git
cd yes-card-sso
```

### 2. Create virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Run the server
```bash
python yes_sso.py
```

Server runs at:
👉 [http://localhost:5000](http://localhost:5000)

---

## 🔗 Endpoints

| Endpoint                                      | Description                                   |
|-----------------------------------------------|-----------------------------------------------|
| `/.well-known/openid-configuration`           | OIDC discovery manifest                       |
| `/authorize?redirect_uri=http://localhost:5000/callback` | Always redirects with `code=dummy-code-1234` |
| `/token` (POST)                               | Always returns static access + ID token       |
| `/userinfo`                                   | Always returns dummy user profile             |
| `/jwks.json`                                  | Dummy JWKS key manifest                       |
| `/callback`                                   | Example client redirect endpoint              |

---

## 🧪 Example Usage

1. **Simulate login redirect**
   ```
   http://localhost:5000/authorize?redirect_uri=http://localhost:5000/callback
   ```
   → Redirects to `/callback?code=dummy-code-1234`

2. **Exchange code for token**
   ```bash
   curl -X POST http://localhost:5000/token
   ```
   Response:
   ```json
   {
     "access_token": "dummy-access-token-1234",
     "token_type": "Bearer",
     "expires_in": 3600,
     "id_token": "dummy-id-token-1234"
   }
   ```

3. **Fetch user info**
   ```bash
   curl http://localhost:5000/userinfo
   ```
   Response:
   ```json
   {
     "sub": "123456",
     "name": "Yes Card User",
     "email": "yescard@example.com",
     "roles": ["admin", "tester"]
   }
   ```

---

## ⚠️ Limitations
- No real security: tokens are **not signed**, no scopes, no PKCE, no error flows.
- Not suitable for production use.
- Intended **only for development/testing**.

---

## 📄 License
MIT — free to use for testing and development.
