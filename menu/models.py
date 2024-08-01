from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('PIZZA', 'PIZZA'),
        ('DRINKS', 'DRINKS'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    photo = models.ImageField(upload_to='dishes/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    likes = models.ManyToManyField(User, related_name='liked_dishes', through='Like')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PIZZA')

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.dish.name}'

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through='OrderItem')
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.dish.name} (x{self.quantity})'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    STATUS_CHOICES = [
        ('', ''),
        ('', ''),
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = 
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dish')