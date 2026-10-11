def send_alert(message: str, severity: str = "warning"):
    print(f"[ALERT] {severity.upper()}: {message}")
    # Integration with Slack/Email would go here
