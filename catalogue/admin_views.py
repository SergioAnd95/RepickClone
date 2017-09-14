from django.views.generic import FormView
from django.core.files import File
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

import io
import os
import itertools

import xlrd
from urllib import request

from .forms import ProccesItemForm
from .models import Item, Brand, Category

from django.core.files import File


class ProcessItemFormView(FormView):
    template_name = 'catalogue/admin/from_file_form.html'
    form_class = ProccesItemForm
    success_url = '/admin/catalogue/item/'

    def form_valid(self, form):
        file = form.cleaned_data['excel_file']
        self.process_item(file)
        return super().form_valid(form)

    def process_item(self, file):
        workbook = xlrd.open_workbook(file_contents=file.read())
        first_sheet = workbook.sheet_by_index(0)

        brands_errors = []
        for row in itertools.islice(first_sheet.get_rows(), 1, None):

            try:
                brand = Brand.objects.get(name=row[0].value)
            except Brand.DoesNotExist:
                brands_errors.append((row[0].value, _('Brand don\'t exist')))
                continue

            categories = Category.objects.filter(
                name__in=row[1].value.split(', '),
                type=1
            )

            gifts = Category.objects.filter(
                name__in=row[2].value.split(', '),
                type=2
            )

            title = row[3].value

            if Item.objects.filter(title=title).exists():
                continue

            item_dict = {
                'title': title,
                'brand': brand,
                'description': row[5].value,
                'in_trend': row[6].value.lower() in ['yes', '+', 'да'],
                'is_prime': row[7].value.lower() in ['yes', '+', 'да'],
                'price': row[8].value,
                'additional_likes': int(row[9].value),
                'link': row[10].value,
                'slug': slugify(title)
            }

            item = Item.objects.create(**item_dict)

            item.categories = list(categories) + list(gifts)

            image_link = row[4].value
            img_resp = request.urlretrieve(image_link)
            print(img_resp)
            item.main_image.save(
                os.path.basename(image_link),
                File(open(img_resp[0], 'rb'))
            )
            item.save()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['opts'] = Item._meta
        return ctx