import feedparser
from groq import Groq
import requests
import json
import time

# ==========================================
# 設定部分（書き換え忘れるなよ！）
# ==========================================
GROQ_API_KEY = "GROQ_API_KEY"
DISCORD_WEBHOOK_URL = "DISCORD_WEBHOOK_URL"

# ニュースの検索条件
RSS_URL = "https://news.google.com/rss/search?q=SaaS+OR+AI&hl=ja&gl=JP&ceid=JP:ja"

# Groqクライアントの設定
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"  # 2026年でも現役の超強力モデルだお

def main():
    print("Groqニキに翻訳をお願いしにいくお...")
    feed = feedparser.parse(RSS_URL)
    
    for entry in feed.entries[:3]:
        title = entry.title
        link = entry.link
        
        # VIPPER化の指示（プロンプト）
        prompt = f"以下のニュースを2chのVIPPER風に3行で要約して。語尾は『〜だお』『〜ンゴ』『草』とか使って。最後に住民を煽る一言を添えて。\nニュース：{title}"
        
        try:
            # Groqでの生成処理だお
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=MODEL_NAME,
            )
            
            summary = chat_completion.choices[0].message.content
            
            payload = {
                "content": f"**【Groq爆速報】AI・SaaSニュースだおｗｗｗ**\n{summary}\nソース：{link}\n--------------------------------"
            }
            
            requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
            print(f"送信成功だお！: {title[:20]}...")
            time.sleep(2)
            
        except Exception as e:
            print(f"Groqでエラーだお：{e}")

if __name__ == "__main__":
    main()