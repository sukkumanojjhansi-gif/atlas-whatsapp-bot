import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google import genai

app = Flask(__name__)

# आपकी नई AQ वाली API Key
API_KEY = "AQ.Ab8RN6UoUmPm_fTZ3cgKY3RzljQz-ryZ8gbGkuimAoZeCco0Q"

try:
    # New official Gemini SDK Client
    client = genai.Client(api_key=API_KEY)
except Exception as init_err:
    client = None

@app.route("/", methods=["GET"])
def home():
    return "Atlas Bot is Live and Healthy!"

@app.route("/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Namaste! Main Atlas AI hoon. Aapka message mujhe mil gaya hai.")
        return str(resp)

    try:
        if client:
            # New generate content syntax
            gemini_res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=incoming_msg
            )
            reply = gemini_res.text.strip()
        else:
            reply = "Atlas Bot: AI Client configure nahi ho paya."
    except Exception as e:
        reply = f"Atlas Bot Error: {str(e)}"

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
