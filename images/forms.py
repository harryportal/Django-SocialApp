from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.')[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match \
            a valid url')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False) # save image without persistence
        image_url = self.cleaned_data['url'] # get the image url
        name = slugify(self.title)
        extension = image_url.split('.')[1].lower()
        image_name = f'{name}.{extension}'

        # download the given image from the given url
        image_file = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(image_file.read()), commit=False)

        if commit:
            image.save()
        return image
