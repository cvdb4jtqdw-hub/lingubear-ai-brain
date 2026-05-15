from flask import Flask, request, jsonify
from flask_cors import CORS
from duckduckgo_search import DDGS
import requests
import time

app = Flask(__name__)
CORS(app)

# ပိုငြိမ်တဲ့ AI Brain Model ကို ပြောင်းထားပါတယ်
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

def internet_search(query):
    try:
        with DDGS() as ddgs:
            # အင်တာနက်က နောက်ဆုံးပေါ် data တွေကို Python နဲ့ ဆွဲယူမယ်
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return "No specific internet data found at the moment."

@app.route('/')
def home():
    return "Lingubear AI Unlimited Brain is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        # ၁။ အင်တာနက်မှာ ရှာမယ်
        web_info = internet_search(prompt)
        
        # ၂။ AI Brain ဆီ ပို့ဖို့ စာသားကို ပိုသေချာအောင် ပြင်မယ်
        full_context = f"<|system|>\nYou are Lingubear AI. Use the following internet data to answer the user.\nData: {web_info}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
        
        # ၃။ AI Brain ကို ခေါ်မယ် (Retry system ပါဝင်တယ်)
        for _ in range(3): # အကယ်၍ ထိုင်းနေရင် ၃ ကြိမ်အထိ ထပ်စမ်းမယ်
            response = requests.post(API_URL, json={"inputs": full_context})
            result = response.json()
            if isinstance(result, list) and 'generated_text' in result[0]:
                ai_reply = result[0]['generated_text'].split("<|assistant|>\n")[-1]
                return jsonify({"reply": ai_reply.strip()})
            time.sleep(2) # ၂ စက္ကန့် စောင့်ပြီး ပြန်စမ်းမယ်

        return jsonify({"reply": "Brain က နိုးကြားလာပါပြီ၊ မေးခွန်းကို တစ်ခေါက်လောက် ပြန်ပို့ပေးပါဦး။"})
    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
