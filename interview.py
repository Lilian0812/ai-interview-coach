import os
import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
MODEL = os.getenv("MODEL", "llama3-70b-8192")

system_prompt = """
你是一位專業的模擬面試官，根據使用者輸入的背景資訊（應徵職缺、自我介紹、專案經驗、技能）
來設計面試問題，必須以全中文台灣話繁體字回應。

請先給一句自然的回應或開場白，再提出問題。
例如：「好的，我看到你有不錯的開發經驗。那麼我想問...」

問題要具體、真實且與職位高度相關，直接提問即可。
"""

feedback_prompt_template = """
你是一位專業的面試官。以下是應徵者的回答:
"{answer}"
請用全中文台灣話提供：
1. 評分:邏輯性、完整度、說服力、專業性、案例具體性（各 10 分，並說明原因）
2. 優點:列出 2-3 個具體的優點（語言表達、邏輯、內容等）
3. 缺點:指出 2-3 個需要改進的地方，提供具體改善建議
4. 整體建議:提供實際可行的改善方式和更好的回答方向，可附上更加的回答範例
"""

context = {"background": "", "question": "", "history": []}

def _post_chat(messages):
    if not API_KEY:
        raise RuntimeError("缺少 GROQ_API_KEY 環境變數")
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": messages},
        timeout=60,
    )
    if resp.status_code != 200:
        return f"API 錯誤 {resp.status_code}：{resp.text}"
    return resp.json()["choices"][0]["message"]["content"]

def generate_question(position, intro, skills, project, difficulty="中級", question_type="技術問題"):
    context["background"] = f"職位：{position}\n自我介紹：{intro}\n技能：{skills}\n專案經驗：{project}"
    prompt = f"{system_prompt}\n以下是使用者背景：\n{context['background']}\n\n請生成一個{difficulty}難度的{question_type}。"
    question = _post_chat([
        {"role": "system", "content": "你是一位專業的模擬面試官"},
        {"role": "user", "content": prompt},
    ])
    context["question"] = question
    return question

def give_feedback(answer):
    prompt = feedback_prompt_template.format(answer=answer)
    feedback = _post_chat([
        {"role": "system", "content": "你是一位專業的面試官"},
        {"role": "user", "content": prompt},
    ])
    context["history"].append({
        "question": context["question"],
        "answer": answer,
        "feedback": feedback
    })
    return feedback