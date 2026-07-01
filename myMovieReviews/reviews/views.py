from django.shortcuts import render, get_object_or_404, redirect
from .models import Review

# Create your views here.
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        release_year = request.POST.get('release_year')
        genre = request.POST.get('genre')
        rating = request.POST.get('rating')
        running_time = request.POST.get('running_time')
        content = request.POST.get('content')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        Review.objects.create(title=title, release_year=release_year, genre=genre, rating=rating, running_time=running_time, content=content, director=director, actor=actor)
        return redirect('review-list')
    return render(request, 'reviews/review_form.html')

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.release_year = request.POST.get('release_year')
        review.genre = request.POST.get('genre')
        review.rating = request.POST.get('rating')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.save()
        return redirect('review-detail', pk=pk)
    return render(request, 'reviews/review_form.html', {'review': review})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review-list')
    return render(request, 'reviews/review_delete.html', {'review': review})