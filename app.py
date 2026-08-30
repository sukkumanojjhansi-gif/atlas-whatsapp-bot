import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# Direct API Configuration
API_KEY = "AQ.Ab8RN6KYM3-YW-rPl_wQioddlooam2BLmvoeqf2ped7plyBT0A"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as init_err:
    model = None

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
        if model:
            # Gemini generation
            gemini_res = model.generate_content(incoming_msg)
            reply = gemini_res.text.strip()
        else:
            reply = "Atlas Bot: AI Model configure nahi ho paya."
    except Exception as e:
        reply = f"Atlas Bot Error: {str(e)}"

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
