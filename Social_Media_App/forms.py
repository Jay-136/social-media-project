from django import forms
from django.forms import ModelForm, RadioSelect
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import *


class SocialAdminForm(ModelForm):
    # first_name = forms.CharField(label="First name", max_length=32)
    # last_name = forms.CharField(label="Last name", max_length=32)

    class Meta:
        model = Post
        fields = [
            'title',
            'image',
            'content',
            'tag',
            'user'
        ]
        widgets = {
            "user": RadioSelect(),
        }
    
    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     try:
    #         content_type = image.content_type
    #         if content_type in settings.CONTENT_TYPES:
    #             if image.size > int(settings.MAX_UPLOAD_SIZE):
    #                 raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
    #         else:
    #             raise forms.ValidationError(_('File type is not supported'))
    #         return image
    #     except AttributeError:
    #         return image