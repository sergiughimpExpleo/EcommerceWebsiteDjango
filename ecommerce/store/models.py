from django.db import models
# the default Django user model to can create a OneToOne relationship
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    # A OneToOne relationship to the User model (A User can have one Customer, a Customer can have one User)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# "Product", "Order" & "OrderItem": 3 essential models that make up the order 
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    # "digital" will let us to know if this is a digital product or a physical product that need to be shipped
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # imageURL Method (if the instance has an image, if not, return an empty string)
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# "Order" will be the summary of items order and a transaction id.
# In Order is sort of like the card and OrderItems will be the items in the cart.
class Order(models.Model):
    # relationship with the Customer -> ManyToOne relationship -> Customer can have multiple orders
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_order = models.DateTimeField(auto_now_add=True)
    # if complete==False: it is a open cart and we can add items to that cart; else: is a closed cart, we need to create items to a different order
    complete = models.BooleanField(default=False, null=True, blank=False)
    # transaction_id -> add some extra information to our Order
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return  str(self.id)
    
# The OrderItem model will be connected to the customer with a one to many relationship (aka ForeignKey) and will hold the status of complete (True or False) and a transaction id along with the date this order was placed.
# The OrderItem will need a Product attribute connected to the product model, the order this item is connected to, quantity and the date this item was added to card.
# A single Order can have multiple "OrderItems"
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

# ShippingAddress will ne a child to Order and will only be created if at least one OrderItem within an order is a physical product 
#   (if Product.digital==False)
# ShippingAddress will be connected to a Customer. A Customer can reuse the shipping address if needed in the future.
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.address