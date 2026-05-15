from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ဒါက ခင်ဗျားရဲ့ ကိုယ်ပိုင် Brain (Mistral Model - Key မလိုပါ)
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/')
def home():
    return "Lingubear AI Brain is Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')

        # AI ဆီ ပို့မယ့် စာသားပြင်ဆင်ချက်
        payload = {
            "inputs": f"<s>[INST] You are Lingubear AI. User says: {user_prompt} [/INST]",
            "parameters": {"max_new_tokens": 500, "return_full_text": False}
        }

        # AI Brain ဆီ လှမ်းမေးမယ်
        response = requests.post(MODEL_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # အဖြေကို ထုတ်ယူမယ်
            reply = result[0]['generated_text']
            return jsonify({"reply": reply.strip()})
        elif response.status_code == 503:
            return jsonify({"reply": "AI Brain က စက်နိုးနေတုန်းမို့ပါ၊ ခဏနေပြန်မေးပေးပါဗျ။"})
        else:
            return jsonify({"reply": "Brain ခဏလေး ထိုင်းနေလို့ပါ၊ နောက်တစ်ခေါက် ပြန်ပို့ပေးပါ။"})

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 200

# Gunicorn အတွက် app ကို export လုပ်ထားတာ သေချာပါစေ
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)

