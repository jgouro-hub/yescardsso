from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)

# Dummy user data
DUMMY_USER = {
    "sub": "123456",
    "name": "Yes Card User",
    "email": "yescard@example.com",
    "roles": ["admin", "tester"]
}

# Dummy OIDC provider config
ISSUER = "http://localhost:5000"

# 1. Discovery document
@app.route("/.well-known/openid-configuration")
def openid_config():
    return jsonify({
        "issuer": ISSUER,
        "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token",
        "userinfo_endpoint": f"{ISSUER}/userinfo",
        "jwks_uri": f"{ISSUER}/jwks.json",
        "response_types_supported": ["code", "token", "id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["none"],  # no signature (yes-card)
    })

# 2. JWKS (normally used to verify tokens) → here dummy
@app.route("/jwks.json")
def jwks():
    # Normally you'd publish real RSA/ECDSA keys
    return jsonify({
        "keys": [
            {
                "kty": "oct",
                "kid": "yescard-key",
                "use": "sig",
                "alg": "HS256",
                "k": "dummy-secret-key-base64"
            }
        ]
    })

# 3. /authorize endpoint
@app.route("/authorize")
def authorize():
    redirect_uri = request.args.get("redirect_uri", url_for("callback", _external=True))
    code = "dummy-code-1234"  # always the same
    return redirect(f"{redirect_uri}?code={code}")

# 4. /token endpoint
@app.route("/token", methods=["POST"])
def token():
    return jsonify({
        "access_token": "dummy-access-token-1234",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "dummy-id-token-1234"  # would normally be JWT
    })

# 5. /userinfo endpoint
@app.route("/userinfo")
def userinfo():
    return jsonify(DUMMY_USER)

# 6. /callback (simulated client app)
@app.route("/callback")
def callback():
    code = request.args.get("code", "dummy-code-1234")
    return f"✅ Logged in with code: {code}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
