def risk_category(score, cutoffs):
    if score >= cutoffs["critical"]: return "CRITICAL", "Prioritize investigation"
    if score >= cutoffs["high"]: return "HIGH", "Flag for security review"
    if score >= cutoffs["medium"]: return "MEDIUM", "Log for investigation"
    return "LOW", "Allow and monitor"
