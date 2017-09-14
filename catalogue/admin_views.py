from django.views.generic import FormView
from django.core.files import File
from django.utils.text import slugify
from django.shortcuts import render
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
        error_ctx  = self.process_item(file)
        if error_ctx:
            return render(self.request, 'catalogue/admin/import_errors.html', error_ctx)
        return super().form_valid(form)

    def process_item(self, file):
        workbook = xlrd.open_workbook(file_contents=file.read())
        first_sheet = workbook.sheet_by_index(0)

        brand_errors = {}
        category_errors = {}
        gift_errors = {}

        for row in itertools.islice(first_sheet.get_rows(), 1, None):
            brand_name = row[0].value
            title = row[3].value

            if Item.objects.filter(title=title).exists():
                continue

            try:
                brand = Brand.objects.get(name=brand_name)
            except Brand.DoesNotExist:
                print('error')
                if brand_name in brand_errors:
                    brand_errors[brand_name]['items_names'].append(title)
                else:
                    brand_errors.update({brand_name:{'items_names': [title], 'error':_('Brand doesn\'t exist')}})
                continue

            categories_names= set(row[1].value.split(', '))
            categories = Category.objects.filter(
                name__in=categories_names,
                type=1
            )

            cat_names = {i.name for i in categories}
            a = categories_names-cat_names
            if a:
                for i in a:
                    if i in category_errors:
                        category_errors[i]['items_names'].append(title)
                    else:
                        category_errors.update({i: {'items_names': [title], 'error': _('Category doesn\'t exist')}})
                continue

            gifts_names = set(row[2].value.split(', '))

            gifts = Category.objects.filter(
                name__in=gifts_names,
                type=2
            )
            gif_names = {i.name for i in gifts}
            a = gifts_names - gif_names
            if a:
                for i in a:
                    if i in gift_errors:
                        gift_errors[i]['items_names'].append(title)
                    else:
                        gift_errors.update({i: {'items_names': [title], 'error': _('Gift doesn\'t exist')}})
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

        if brand_errors or category_errors or gift_errors:
            return {
                'brand_errors': brand_errors,
                'category_errors': category_errors,
                'gift_errors': gift_errors,
                'opts': Item._meta
            }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['opts'] = Item._meta
        return ctx