from .forms import ImageForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            # associate image with the current user
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'New Image added successfully')
            return redirect(new_image.get_absolute_url)
    else:
        form = ImageForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section':'images', 'form':form})



