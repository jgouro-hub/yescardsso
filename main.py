from flask import Flask, request, jsonify, redirect, url_for, render_template_string, abort

app = Flask(__name__)

# -------------------------------------------------------------------
# Dummy OIDC provider config
ISSUER = "http://localhost:5000"
SUPPORTED_SCOPES = ["openid", "profile", "email", "account", "services", "rights"]

# Default Salesforce scratch org admin email
DEFAULT_EMAIL = "admin@scratchorg.com"

# -------------------------------------------------------------------
# Discovery document
@app.route("/.well-known/openid-configuration")
def openid_config():
    return jsonify({
        "issuer": ISSUER,
        "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token",
        "userinfo_endpoint": f"{ISSUER}/userinfo",
        "jwks_uri": f"{ISSUER}/jwks.json",
        "scopes_supported": SUPPORTED_SCOPES,
        "response_types_supported": ["code", "token", "id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["none"],
        "claims_supported": ["sub", "name", "firstName", "lastName", "email", "account", "services", "rights"]
    })

# -------------------------------------------------------------------
# Dummy JWKS
@app.route("/jwks.json")
def jwks():
    return jsonify({
        "keys": [
            {
                "kty": "oct",
                "kid": "e2e-oidc-key",
                "use": "sig",
                "alg": "HS256",
                "k": "dummy-secret-key-base64"
            }
        ]
    })

# -------------------------------------------------------------------
# Authorization endpoint (with login form)
@app.route("/authorize")
def authorize():
    redirect_uri = request.args.get("redirect_uri", url_for("callback", _external=True))
    state = request.args.get("state", "")
    scope = request.args.get("scope", "openid profile email")

    # ✅ Guard for Salesforce scratch org redirect
    if "scratch.my.salesforce.com" not in redirect_uri:
        abort(500, description="Invalid redirect_uri (must include scratch.my.salesforce.com)")

    form_html = f"""
    <html>
      <body>
        <h2>E2E OIDC Login</h2>
        <form method="post" action="/login">
          <input type="hidden" name="redirect_uri" value="{redirect_uri}">
          <input type="hidden" name="state" value="{state}">
          <input type="hidden" name="scope" value="{scope}">
          Email: <input type="text" name="email" value="{DEFAULT_EMAIL}"><br>
          <button type="submit">Login</button>
        </form>
      </body>
    </html>
    """
    return render_template_string(form_html)

@app.route("/login", methods=["POST"])
def login():
    redirect_uri = request.form["redirect_uri"]
    state = request.form.get("state", "")
    email = request.form.get("email", DEFAULT_EMAIL)

    # ✅ Guard again (POST flow)
    if "scratch.my.salesforce.com" not in redirect_uri:
        abort(500, description="Invalid redirect_uri (must include scratch.my.salesforce.com)")

    # Encode email into "code"
    code = f"dummy-code-{email}"

    return redirect(f"{redirect_uri}?code={code}&state={state}")

# -------------------------------------------------------------------
# Token endpoint
@app.route("/token", methods=["POST"])
def token():
    code = request.form.get("code", "")
    scope = request.form.get("scope", "openid profile email")

    # Extract email from code, fallback to default
    if code.startswith("dummy-code-"):
        email = code.replace("dummy-code-", "")
    else:
        email = DEFAULT_EMAIL

    access_token = f"dummy-access-token-for-{email}"

    user = {
        "sub": "123456",
        "name": "E2E OIDC User",
        "email": email,
        "lastName": "Assurance",
        "firstName": "Quality",
        "account": "ACME Corp",
        "services": ["EQCORPORATEPLUS"],
        "rights": ["read", "write", "delete"]
    }

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": f"dummy-id-token-for-{email}",
        "userinfo": user
    })

# -------------------------------------------------------------------
# Userinfo endpoint
@app.route("/userinfo")
def userinfo():
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        token = ""

    # Extract email from dummy token
    if token.startswith("dummy-access-token-for-"):
        email = token.replace("dummy-access-token-for-", "")
    else:
        email = DEFAULT_EMAIL

    return jsonify({
        "sub": "123456",
        "name": "E2E OIDC User",
        "lastName": "Assurance",
        "firstName": "Quality",
        "email": email,
        "account": "ACME Corp",
        "services": ["EQCORPORATEPLUS"],
        "rights": ["read", "write", "delete"]
    })

# -------------------------------------------------------------------
# Callback (for manual testing in browser)
@app.route("/callback")
def callback():
    code = request.args.get("code", "dummy-code-1234")
    state = request.args.get("state", "")
    return f"✅ Logged in with code={code}, state={state}"

# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
