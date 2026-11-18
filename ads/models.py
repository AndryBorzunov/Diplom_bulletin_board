from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Категория товара",
        help_text="Укажите категорию товара",
    )

    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ad(models.Model):
    STATUS_CHOICES = [
        ("published", "Опубликовано"),
        ("sold", "Продано"),
        ("draft", "Черновик"),
    ]
    CONDITION_CHOICES = [("new", "Новый"), ("used", "Б/у")]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="ads")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="published"
    )
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="used"
    )
    city = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["category", "status"]),
        ]

    def __str__(self):
        return self.title
