def validate_token(token):
    from routes.auth import tokens
    return token in tokens
