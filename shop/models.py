from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
class Customize(models.Model):
    name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=100)
    dimensions=models.CharField(max_length=10)
    img=models.ImageField(upload_to='shop/artworks')
    date=models.DateField()


class Artwork(models.Model):
    art_name=models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    artist_name=models.CharField(max_length=100)
    pub_date=models.DateField()
    price=models.IntegerField()
    dimension=models.CharField(max_length=100,default="")
    image=models.ImageField(upload_to='shop/artworks')
    slug=models.SlugField(default="")

    def __str__(self):
        return self.art_name

    def get_absolute_url(self):
        return reverse("shop:view",kwargs={
            'slug':self.slug
        })

    @property
    def imageURL(self):
        try:
           url = self.image.url
        except:
           url = ''
        return url

class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    #@property
    #def shipping(self):
    #    shipping=True
    #    return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Artwork, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
