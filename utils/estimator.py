def estimate_project(user_message: str) -> str:
    """
    Generate project estimation based on the description requested by the user.
    """

    message = user_message.lower()

    # Quick rules
    if "gym" in message and "website" in message:
        return _gym_website_estimate()
    if "ecommerce" in message:
        return _ecommerce_estimate()
    if "blog" in message:
        return _blog_estimate()
    if "portfolio" in message:
        return _portfolio_estimate()

    # General Website Estimation
    if "website" in message:
        return _generic_website_estimate()

    # General App Estimation
    if "app" in message:
        return _generic_app_estimate()

    return "I can help with a project estimation. Please tell me what kind of website or app you want."


# -------------------------------  
#  Specific Estimation Templates  
# -------------------------------  

def _gym_website_estimate():
    return """
🏋️ PROJECT ESTIMATE: GYM WEBSITE

📌 Key Features:
• Home page with gym intro  
• Trainer profiles  
• Membership plans  
• Contact form  
• Gallery  
• Optional: Online booking system

⏳ Estimated Timeline:
• UI Design: 2 days  
• Frontend Development: 3 days  
• Backend + Database: 2–3 days  
• Testing & Deployment: 1 day  

👉 Total: **7–9 days**

💰 Cost not included as per your requirement.
"""

def _ecommerce_estimate():
    return """
🛒 PROJECT ESTIMATE: E-COMMERCE PLATFORM

📌 Key Features:
• Product listing  
• Search & filters  
• Cart + Checkout  
• User login/Signup  
• Admin panel  
• Order management

⏳ Estimated Timeline:
• Design: 3–4 days  
• Frontend: 5–7 days  
• Backend + Database: 6–10 days  
• Testing: 2–3 days  

👉 Total: **16–24 days**
"""

def _blog_estimate():
    return """
📝 PROJECT ESTIMATE: BLOG WEBSITE

📌 Key Features:
• Posts listing  
• Categories  
• Admin blog editor  
• Comments section  
• SEO friendly

⏳ Estimated Timeline:
• Design: 1–2 days  
• Development: 4–5 days  
• Testing + Deployment: 1 day  

👉 Total: **6–8 days**
"""

def _portfolio_estimate():
    return """
👤 PROJECT ESTIMATE: PORTFOLIO WEBSITE

📌 Features:
• About section  
• Projects showcase  
• Contact form  
• Resume download

⏳ Timeline: **3–4 days**
"""

def _generic_website_estimate():
    return """
🌐 GENERAL WEBSITE ESTIMATION

📌 Please specify:
• Type of website (gym, hospital, school, ecommerce, etc.)  
• Number of pages  
• Any special features

⏳ Typical Timeline:
• Simple website: **3–5 days**  
• Medium website: **7–10 days**  
• Advanced (login, dashboard): **14–20 days**
"""

def _generic_app_estimate():
    return """
📱 GENERAL APP DEVELOPMENT ESTIMATION

⏳ Timeline:
• Simple app: 10–15 days  
• Medium app: 20–30 days  
• Complex app: 40–60 days

💡 Tell me the app type and features for a detailed timeline.
"""
