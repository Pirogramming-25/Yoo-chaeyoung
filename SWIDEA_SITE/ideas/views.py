from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea
from devtools.models import Devtool

# Create your views here.
def main(request):
    ideas = Idea.objects.all()
    return render(request, "ideas/main.html", {'ideas': ideas})


def idea_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        interest = request.POST.get('interest')

        devtool_id = request.POST.get('devtool')
        devtool_obj = get_object_or_404(Devtool, pk=devtool_id) if devtool_id else None

        Idea.objects.create(
            title=title, image=image, content=content, interest=interest, devtool=devtool_obj
        )

        return redirect('idea-list')
    
    devtools = Devtool.objects.all()
    return render(request, "ideas/idea_form.html", {'devtools': devtools})


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, "ideas/idea_detail.html", {'idea': idea})


def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        idea.title = request.POST.get('title')

        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')

        idea.content = request.POST.get('content')
        idea.interest = request.POST.get('interest')

        devtool_id = request.POST.get('devtool')
        if devtool_id :
            idea.devtool = get_object_or_404(Devtool, pk=devtool_id)
        else: 
            idea.devtool = None

        idea.save()

        return redirect('idea-detail', pk=pk)
    
    devtools = Devtool.objects.all()
    return render(request, "ideas/idea_form.html", {'devtools': devtools})