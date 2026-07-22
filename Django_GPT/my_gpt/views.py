import logging
from django.shortcuts import render
from .models import InferenceHistory
from .decorators import model_login_required
from .services.sentiment import run_sentiment
from .services.summarizer import run_summarize
from .services.moderator import run_moderate
from .services.combo import run_combo

logger = logging.getLogger(__name__)


def sentiment_view(request):
    result = None
    error = None
    histories = []

    if request.user.is_authenticated:
        histories = InferenceHistory.objects.filter(
            user=request.user, task=InferenceHistory.Task.SENTIMENT
        )[:5]

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            error = "분석할 문장을 입력해주세요."
        elif len(text) > 1000:
            error = "문장은 1,000자 이하로 입력해주세요."
        else:
            try:
                result = run_sentiment(text)
                if request.user.is_authenticated:
                    InferenceHistory.objects.create(
                        user=request.user,
                        task=InferenceHistory.Task.SENTIMENT,
                        input_text=text,
                        output_text=f"감정: {result['top_label']}, 신뢰도: {result['top_score']}",
                        result_data=result,
                    )
            except Exception:
                logger.exception("Sentiment Model Error")
                error = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."

    return render(
        request,
        "my_gpt/sentiment.html",
        {
            "result": result,
            "error": error,
            "histories": histories,
            "active_tab": "sentiment",
        },
    )


@model_login_required
def summarize_view(request):
    result = None
    error = None
    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.SUMMARIZE
    )[:5]

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if len(text) < 100:
            error = "요약할 문서는 100자 이상 입력해주세요."
        elif len(text) > 5000:
            error = "문서는 5,000자 이하로 입력해주세요."
        else:
            try:
                result = run_summarize(text)
                InferenceHistory.objects.create(
                    user=request.user,
                    task=InferenceHistory.Task.SUMMARIZE,
                    input_text=text,
                    output_text=result["summary"],
                    result_data=result,
                )
            except Exception:
                logger.exception("Summarize Model Error")
                error = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."

    return render(
        request,
        "my_gpt/summarize.html",
        {
            "result": result,
            "error": error,
            "histories": histories,
            "active_tab": "summarize",
        },
    )


@model_login_required
def moderate_view(request):
    result = None
    error = None
    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.MODERATE
    )[:5]

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            error = "분석할 문장을 입력해주세요."
        elif len(text) > 1000:
            error = "문장은 1,000자 이하로 입력해주세요."
        else:
            try:
                result = run_moderate(text)
                InferenceHistory.objects.create(
                    user=request.user,
                    task=InferenceHistory.Task.MODERATE,
                    input_text=text,
                    output_text=f"최고 위험: {result['top_label']}, 점수: {result['top_score']}",
                    result_data=result,
                )
            except Exception:
                logger.exception("Moderate Model Error")
                error = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."

    return render(
        request,
        "my_gpt/moderate.html",
        {
            "result": result,
            "error": error,
            "histories": histories,
            "active_tab": "moderate",
        },
    )


@model_login_required
def combo_view(request):
    result = None
    error = None
    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.COMBO
    )[:5]

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if len(text) < 200:
            error = "복합 분석 문장은 200자 이상 입력해주세요."
        elif len(text) > 5000:
            error = "문서는 5,000자 이하로 입력해주세요."
        else:
            try:
                result = run_combo(text)
                InferenceHistory.objects.create(
                    user=request.user,
                    task=InferenceHistory.Task.COMBO,
                    input_text=text,
                    output_text=result["summary"]["summary"],
                    result_data=result,
                )
            except Exception:
                logger.exception("Combo Model Error")
                error = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."

    return render(
        request,
        "my_gpt/combo.html",
        {
            "result": result,
            "error": error,
            "histories": histories,
            "active_tab": "combo",
        },
    )