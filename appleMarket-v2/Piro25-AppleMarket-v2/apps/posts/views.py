from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post
from .forms import PostForm

from .services.ocr_service import extract_text_from_image
from .services.rules import parse_nutrition_info


def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)


def create(request):
    if request.method == 'GET':
        form = PostForm()
        context = { 'form': form }
        return render(request, 'posts/create.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')


def detail(request, pk):
    target_post = Post.objects.get(id=pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)


def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form, 
            'post': post
        }
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')


@require_POST
def process_ocr(request):
    if 'nutrition_image' not in request.FILES:
        return JsonResponse({'success': False, 'error': '이미지가 없습니다.'}, status=400)

    image_file = request.FILES['nutrition_image']
    
    try:
        # 1. OCR 텍스트 추출
        extracted_texts = extract_text_from_image(image_file)
        print("=== [1. 추출된 텍스트] ===", extracted_texts)
        
        # 2. 영양성분 파싱
        nutrition_data = parse_nutrition_info(extracted_texts)
        print("=== [2. 파싱 결과 데이터] ===", nutrition_data)
        
        # None 값을 빈칸 대신 기본 0 또는 인식 수치로 전달
        cleaned_data = {
            'calories': nutrition_data.get('calories') if nutrition_data.get('calories') is not None else 0,
            'carbs': nutrition_data.get('carbs') if nutrition_data.get('carbs') is not None else 0,
            'protein': nutrition_data.get('protein') if nutrition_data.get('protein') is not None else 0,
            'fat': nutrition_data.get('fat') if nutrition_data.get('fat') is not None else 0,
        }

        return JsonResponse({
            'success': True,
            'data': cleaned_data
        })
    except Exception as e:
        print(f"❌ OCR 처리 중 오류 발생: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)