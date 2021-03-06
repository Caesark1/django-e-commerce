from django.db import models


class CategoryFeature(models.Model):
    """
    Характеристики конкретной категории
    """
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100)
    feature_filter_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f"{self.feature} for {self.category.name}"


class FeatureValidator(models.Model):
    """
    Валидатор значений для контретной характеристики, принадлежащей конкретной категории
    """

    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100)

    def __str__(self):
        return f'Категория - {self.category.name} -- Характеристики - {self.feature_key.feature_name}-- ' \
               f'Валидное значение {self.valid_feature_value}'


class ProductFeatures(models.Model):
    """
    Характеристика товаров
    """
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=30)

    def __str__(self):
        return f'Товар - {self.product.title} -- ' \
               f'Характеристики - {self.feature.feature_name}' \
               f'Значение - {self.value}'
