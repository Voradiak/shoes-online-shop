from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Shoe', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'

class Shoe(models.Model):
    image = models.ImageField(upload_to='shoeimg/', blank=False, null=False, verbose_name='Shoe image')
    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(blank=False)
    description = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}  {self.price}$' 
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product')
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product')
        
    def total_price(self):
        return self.product.price * self.quantity
# Create your models here.
