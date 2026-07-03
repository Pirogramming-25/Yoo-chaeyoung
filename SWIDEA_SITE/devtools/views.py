from django.shortcuts import render, get_object_or_404, redirect
from .models import Devtool

# Create your views here.
def devtool_list(request):
    devtools = Devtool.objects.all()
    return render(request, "devtools/devtool_list.html", {'devtools': devtools})


def devtool_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        content = request.POST.get('content')

        Devtool.objects.create(
            name=name, kind=kind, content=content
        )

        return redirect('devtool-list')
    return render(request, "devtools/devtools_form.html")


def devtool_detail(request, pk):
    devtool = get_object_or_404(Devtool, pk=pk)
    return render(request, "devtools/devtool_detail.html", {'devtool': devtool})


def devtool_update(request, pk):
    devtool = get_object_or_404(Devtool, pk=pk)
    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.content = request.POST.get('content')

        devtool.save()

        return redirect('devtool-detail', pk=pk)
    
    return render(request, "devtools/devtool_form.html")