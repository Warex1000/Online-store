from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError  # import forms
from django.contrib import admin
from django.utils.safestring import mark_safe  # for highlight an exceptions in class NoteBookAdminForm
from .models import *   # import all models here


class NoteBookAdminForm(ModelForm):  # requirements for save images upper then 400px/lower 900px/lower 3MB for Form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(  # mark_safe transfer python format to css and change color
            """<span style="color:red; font-size:14px;">
            При загрузке изображения с разрешением больше {}x{} оно будет обрезано!
            </span>""".format(*Product.MAX_RESOLUTIONS)
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTIONS
    #     max_height, max_width = Product.MAX_RESOLUTIONS
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображения не должен привышать 3MB')
    #     if img.height < min_height or img.width < min_width:
    #         raise ValidationError('Разрешение изображения меньше минимального')
    #     if img.height > max_height or img.width > max_width:
    #         raise ValidationError('Разрешение изображения больше максимального')
    #     return image


class NotebookAdmin(admin.ModelAdmin):

    form = NoteBookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
            # create notebook goods only in notebooks category
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
            # create smartphone goods only in smartphone category
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)   # Register models in admin panel.
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
# Add SmartphoneAdmin for create smartphone goods only in smartphone category
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
