# ================= FIREWALL MODULE =================

def firewall_check(code):
    """
    Basic firewall to block unsafe / dangerous commands
    """

    code = code.lower()

    blocked_keywords = [
        "os.system",
        "subprocess",
        "import os",
        "import subprocess",
        "rm -rf",
        "format",
        "while(true)",
        "while (true)",
        "__import__"
    ]

    for word in blocked_keywords:
        if word in code:
            return False, f"🚫 Blocked by Firewall: '{word}' detected"

    return True, "✅ Code Safe"