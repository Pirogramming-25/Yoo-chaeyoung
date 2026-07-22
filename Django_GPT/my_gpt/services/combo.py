from .sentiment import run_sentiment
from .summarizer import run_summarize
from .moderator import run_moderate


def run_combo(text):
    summary_res = run_summarize(text)
    summarized_text = summary_res["summary"]

    sentiment_res = run_sentiment(summarized_text)
    moderator_res = run_moderate(text)

    return {
        "summary": summary_res,
        "sentiment": sentiment_res,
        "toxicity": moderator_res,
    }