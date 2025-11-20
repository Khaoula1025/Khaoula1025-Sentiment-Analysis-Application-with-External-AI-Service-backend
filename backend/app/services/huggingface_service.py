import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://router.huggingface.co/hf-inference/models/nlptown/bert-base-multilingual-uncased-sentiment"

async def predict_sentiment(text: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API_URL,
                headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
                json={"inputs": text},
                timeout=30.0
            )
            response.raise_for_status()
            
            max_pred = max(response.json()[0], key=lambda x: x['score'])
            score = int(max_pred['label'].split()[0])
            
            sentiment = "negatif" if score <= 2 else "neutre" if score == 3 else "positif"
            
            return {"score": score, "sentiment": sentiment, "confidence": round(max_pred['score'], 4)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))