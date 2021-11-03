from django import template
from django.utils.safestring import mark_safe
# for read text as a html code

register = template.Library()  # add template to library


TABLE_HEAD = '''
        <table class ="table">        
            <tbody>
'''


TABLE_CONTENT = '''
            <tr>
                <td>{name}</td>
                <td>{value}</td>
            </tr>
'''


TABLE_TAIL = '''
        </tbody>
    </table>
'''


PRODUCT_SPEC = {
    'notebook': {  # Name of model notebook
        'Диагональ': 'diagonal',
        'Дисплей': 'display_type',
        'Процессор': 'processor_freq',
        'Оперативная память': 'ram',
        'Видео Карта': 'video',
        'Время работы от аккумулятора': 'time_without_charge',
    },
    'smartphone': {  # Name of model smartphone
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение екрана': 'resolution',
        'Обем батареи': 'accum_volume',
        'Оперативная память': 'ram',
        'Поддержка CD карты': 'sd',
        'Максимальный обем встроеной памяти': 'sd_volume_max',
        'Главная камера': 'main_camp_mp',
        'Фронтальная камера': 'frontal_camp_mp',
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter   # Create filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
