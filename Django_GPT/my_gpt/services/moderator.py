from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device, get_hf_token


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,
        device=get_pipeline_device(),
        token=get_hf_token(),
    )


def run_moderate(text):
    pipe = get_moderator_pipeline()
    results = pipe(text)

    if isinstance(results, list) and len(results) > 0:
        if isinstance(results[0], list):
            results = results[0]

    sorted_res = sorted(results, key=lambda x: x["score"], reverse=True)
    top_result = sorted_res[0]

    return {
        "top_label": top_result["label"],
        "top_score": f"{top_result['score'] * 100:.2f}%",
        "all_scores": [
            {
                "label": item["label"],
                "score": f"{item['score'] * 100:.2f}%",
            }
            for item in sorted_res
        ],
    }