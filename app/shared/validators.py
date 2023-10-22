def validString(string: str) -> bool:
    string = string.strip().lower()
    if len(string) < 1:
        return False
    return True
