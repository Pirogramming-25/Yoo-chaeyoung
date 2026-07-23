function showLoading() {
    const loadingElem = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');

    if (loadingElem) {
        loadingElem.style.display = 'block';
    }

    if (submitBtn) {
        submitBtn.disabled = true;
    }
}