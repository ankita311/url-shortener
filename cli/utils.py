from pathlib import Path

def get_token_path():
    return Path.home() / ".urlshortener" / "token.txt"

def get_saved_token():
    token_path = get_token_path()
    if token_path.exists():
        return token_path.read_text().strip()
    return None

def delete_token():
    token_path = get_token_path()
    if token_path.exists():
        token_path.unlink()