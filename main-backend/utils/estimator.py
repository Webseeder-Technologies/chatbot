def estimate_project(message: str):
    message = message.lower()

    if "gym website" in message or "fitness website" in message:
        return {
            "project": "Gym Website",
            "time": "7–10 days",
            "features": [
                "Homepage",
                "Trainer Details",
                "Membership Plans",
                "BMI Calculator",
                "Contact Form",
                "Admin Panel"
            ]
        }

    if "portfolio" in message:
        return {
            "project": "Portfolio Website",
            "time": "2–4 days",
            "features": ["About", "Projects", "Skills", "Contact Form"]
        }

    if "ecommerce" in message or "e-commerce" in message:
        return {
            "project": "E-commerce Store",
            "time": "15–25 days",
            "features": ["Authentication", "Cart", "Payments", "Admin Panel"]
        }

    return None
