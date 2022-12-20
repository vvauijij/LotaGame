import re


def get_command_text(text):
    matches = re.search(r'(^/[A-Za-z_]+ )(.*)', text)
    if matches and matches[2] and len(matches[2]) <= 20:
        return matches[2]
    else:
        return None
