import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

# ==========================
# LOAD ENVIRONMENT VARIABLES
# ==========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

print("API Loaded: True")

# ==========================
# LOAD SOP DATA
# ==========================

with open("sop_data.json", "r", encoding="utf-8") as file:
    sop_data = json.load(file)

# ==========================
# SYSTEM PROMPT
# ==========================

SYSTEM_PROMPT = f"""
You are a customer support assistant for {sop_data['business']}.

RULES:

1. Answer ONLY using information found in the SOP.
2. Never invent or assume information.
3. If information is not available in SOP:
   - Say you do not have that information.
   - Escalate to a human agent.
4. Escalate immediately for:
   - complaints
   - medical questions
   - pricing negotiation
   - requests for a human agent.
5. Be friendly, professional, and concise.

SOP DATA:
{sop_data}
"""

conversation_history = []
lead_data = {}

# ==========================
# ESCALATION DETECTION
# ==========================

def check_escalation(message):

    triggers = [
        "complaint",
        "angry",
        "frustrated",
        "refund",
        "manager",
        "human",
        "doctor",
        "medical"
    ]

    msg = message.lower()

    for trigger in triggers:
        if trigger in msg:
            return True, trigger

    return False, None

# ==========================
# AI RESPONSE
# ==========================

def ask_ai(question):

    prompt = f"""
{SYSTEM_PROMPT}

Customer Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error communicating with Gemini API: {str(e)}"

# ==========================
# LEAD QUALIFICATION
# ==========================

def qualify_lead():

    print("\n==============================")
    print("LEAD QUALIFICATION")
    print("==============================")

    lead_data["business_type"] = input(
        "What type of business do you run? "
    )

    lead_data["team_size"] = input(
        "How many employees do you have? "
    )

    lead_data["current_tools"] = input(
        "What tools are you currently using? "
    )

# ==========================
# SUMMARY GENERATION
# ==========================

def generate_summary():

    prompt = f"""
Conversation:
{conversation_history}

Lead Details:
{lead_data}

Generate a structured report with:

1. Customer Intent
2. Key Details Collected
3. SOP Gaps Identified
4. Recommended Next Action
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Summary generation failed: {str(e)}"

# ==========================
# MAIN CHAT LOOP
# ==========================

print("=" * 50)
print("Bloom Aesthetics Clinic Support Bot")
print("=" * 50)

while True:

    user = input("\nCustomer: ")

    if user.lower() == "exit":
        break

    conversation_history.append(
        f"Customer: {user}"
    )

    escalate, reason = check_escalation(user)

    if escalate:

        bot_reply = (
            f"This conversation has been escalated "
            f"to a human representative.\n"
            f"Reason: {reason}"
        )

    else:

        bot_reply = ask_ai(user)

    print("\nAI:", bot_reply)

    conversation_history.append(
        f"AI: {bot_reply}"
    )

# ==========================
# LEAD QUALIFICATION
# ==========================

qualify_lead()

# ==========================
# SUMMARY
# ==========================

summary = generate_summary()

print("\n")
print("=" * 50)
print("CONVERSATION SUMMARY")
print("=" * 50)

print(summary)