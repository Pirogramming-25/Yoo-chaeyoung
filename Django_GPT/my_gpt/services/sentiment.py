from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=get_pipeline_device(),
    )


def run_sentiment(text):
    pipe = get_sentiment_pipeline()
    results = pipe(text, top_k=None)
    sorted_res = sorted(results, key=lambda x: x["score"], reverse=True)
    top_result = sorted_res[0]

    return {
        "top_label": top_result["label"].capitalize(),
        "top_score": f"{top_result['score'] * 100:.2f}%",
        "all_scores": [
            {
                "label": item["label"].capitalize(),
                "score": f"{item['score'] * 100:.2f}%",
            }
            for item in sorted_res
        ],
    }