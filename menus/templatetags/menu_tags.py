from django import template
from django.urls import reverse, NoReverseMatch

from menus.models import MenuItem

register = template.Library()


@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    item_dict = {}
    root_items = []

    for item in items:
        try:
            url = reverse(item.named_url) if item.named_url else item.url
        except NoReverseMatch:
            url = item.url
        item.url = url
        item.is_active = False
        item.is_open = False
        item_dict[item.id] = item
        print(f"Создан элемент: {item.title} с url: {item.url} и родитель: {item.parent}")

    for item in items:
        if not item.parent:
            root_items.append(item)

    active_item = None
    for item in items:
        if item.url == current_path:
            item.is_active = True
            active_item = item
            print(f"Активный пункт: {item.title}")
            break

    if active_item:
        parent = active_item.parent
        while parent:
            parent.is_open = True
            print(f"Родитель развернут: {parent.title}")
            parent = parent.parent

        # Первый уровень детей (теперь доступно через связь)
        for child in active_item.children.all():
            child.is_open = True
            print(f"Дитя развернуто: {child.title}")

    return {'menu': root_items}
