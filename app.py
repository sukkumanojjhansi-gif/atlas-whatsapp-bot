import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Aap Atlas AI hain. Hindi aur Hinglish me helpful jawab dein."
    )
else:
    model = None

@app.route("/", methods=["GET"])
def home():
    return "Atlas AI WhatsApp Bot is Running 24/7!"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Namaste! Main Atlas AI hoon. Bataiye kya madad kar sakta hoon?")
        return str(resp)

    try:
        if model:
            response = model.generate_content(incoming_msg)
            reply_text = response.text.strip()
        else:
            reply_text = "API Key error."
    except Exception as e:
        reply_text = f"Error: {str(e)}"

    msg.body(reply_text)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)