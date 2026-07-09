from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Idea, IdeaStar
from devtools.models import Devtool

# Create your views here.
def idea_list(request):
    sort_by = request.GET.get('sort', 'latest')

    if sort_by == 'interest':
        ideas = Idea.objects.all().order_by('-interest')
    elif sort_by == 'name':
        ideas = Idea.objects.all().order_by('title')
    elif sort_by == 'oldest':
        ideas = Idea.objects.all().order_by('created_at')
    else :
        ideas = Idea.objects.all().order_by('-id')

    context = {
        'ideas': ideas,
        'current_sort': sort_by
    }
    return render(request, "ideas/idea_list.html", context)

@csrf_exempt
def toggle_star(request, pk):
    if request.method == "POST":
        idea = get_object_or_404(Idea, pk=pk)
        star, created = IdeaStar.objects.get_or_create(idea=idea)
        
        if created:
            star.is_starred = True
        else:
            star.is_starred = not star.is_starred
            
        star.save()
        
        return JsonResponse({
            'success': True, 
            'is_starred': star.is_starred
        })
    return JsonResponse({'success': False}, status=400)

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

        return redirect('ideas:idea-list')
    
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

        return redirect('ideas:idea-detail', pk=pk)
    else:
        context = {
            "idea": idea,
            "devtools": Devtool.objects.all()
        }
        return render(request, "ideas/idea_form.html", context)
    
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    
    return redirect("ideas:idea-list")