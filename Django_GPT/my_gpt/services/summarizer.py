from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device, get_hf_token

@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-6-6",
        device=get_pipeline_device(),
        token=get_hf_token(),
    )

def run_summarize(text):
    pipe = get_summarizer_pipeline()
    summary_text = pipe(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    orig_len = len(text)
    summ_len = len(summary_text)
    ratio = (summ_len / orig_len) * 100 if orig_len > 0 else 0
    
    return {
        "summary": summary_text,
        "original_len": orig_len,
        "summary_len": summ_len,
        "ratio": f"{ratio:.2f}%"
    }