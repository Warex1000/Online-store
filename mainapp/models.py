from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model  # v.1 Используем юзера, который указан в настройках
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()  # v.1.1 Используем юзера, который указан в скрытых настройках (settings.AUTH_USER_MODEL)

# ***************
# Создаем модели для интернет-магазина
# 1 Category
# 2 Product
# 3 CartProduct
# 4 Cart
# 5 Order
# 6 Customer
# 7 Spesification
# ***************

"""
# Представление которое будет отвечать за стартовую страницу будет имитировать 1 запрос и доставать вест список
товаров которое мы хотим отобразить на главной странице class LatestProductsManager
ContentType Микрофрейм ворк который видет модели которые есть в INSTALLED_APPS в settings предоставляя 
универсальный интерфейс
"""


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:  # 1:13:00 Просмотреть суть этого класса с моделями.

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')  # Отображение определенных товаров первыми в списке
        products = []  # Финальный список товаров
        ct_models = ContentType.objects.filter(
            model__in=args)  # Запрос ContentType фильтруя модели которые находятся в аргументах args
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.strtswith(with_respect_to),
                        reverse=True)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(
        unique=True)
    ''' 
    короткое название-метка, содержит только буквы числа нижнее подчеркивание дефис. 
    Используются в URL(Category/nootebook)
    '''
    prepopulated_fields = {"slug": (
    "title",)}  # позволяет определить поля, которые получают значение основываясь на значениях других полей

    def __str__(self):  # отображение категории в админке
        return self.name


class Product(models.Model):

    MIN_RESOLUTIONS = (400, 400)
    MAX_RESOLUTIONS = (900, 900)
    MAX_IMAGE_SIZE = 3145728  # ~ 3mb

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.CASCADE)
    '''
    Обект Category класса Product наследуеться(связан) от класса Category / 
    при удалении обекта удаляеться все связи с ним (данные)  
                                 '''
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание товара', null=True)  # Поле может быть пустым null=True
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена'
    )  # Параметры цены, максимальное колличество символов до запятой(9) и после(2)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # requirements for save images upper then 400px and lower then 900px for Shell
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTIONS
        max_height, max_width = self.MAX_RESOLUTIONS
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Разрешение изображения меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Разрешение изображения больше максимального')
        return image


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккамулятора')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)   # {Категория} : {Какой товар}


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение екрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Обьем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный обем встроенной памяти')
    main_camp_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_camp_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    '''
    Микрофрейм ворк который видет модели которые есть в INSTALLED_APPS в settings предоставляя универсальный интерфейс
    '''
    object_id = models.PositiveIntegerField()  # Индификатор инстанс этой модели
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    '''
    Колличество выбранного товара в корзине, по умолчанию 1, Подобно IntegerField, но должно быть либо положительным, 
    либо нулевым (0). Значения от 0 до 2147483647 безопасны во всех базах данных, поддерживаемых Django.
    '''
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Цена')  # Финальная цена всех товаров в корзине

    def __str__(self):
        return "Продукт: {} (для корзины)".format(
            self.product.title)  # !!! Неразрешенная ссылка на атрибут "title" для класса "ForeignKey"


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct,
        blank=True,
        related_name='related_cart'
    )  # Связь многие ко многим к CartProduct
    total_products = models.PositiveIntegerField(default=0)  # Корректное колличество товаров в корзине шт.
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):  # Показываем в админке что это за покупатель
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

#   !!! Change type fields were it must be integer or float, then we do filter on Options
