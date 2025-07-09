from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='название товара')
    price = models.CharField(max_length=10, verbose_name='цена')
    # price_sale = models.CharField(max_length=10, verbose_name='цена со скидкой')
    rating = models.CharField(max_length=10, verbose_name='рейтинг')
    count_comment = models.CharField(max_length=10, verbose_name='количество отзывов')

    def __str__(self):
        return self.name

