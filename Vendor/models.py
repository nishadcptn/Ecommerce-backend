from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    phone = models.CharField(max_length=10, unique=True, null=True)
    token = models.TextField(null=True, blank=True)
    salt = models.TextField(null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'


class Organization(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=220)
    type = models.CharField(max_length=220)
    user_count = models.IntegerField()
    address = models.TextField()
    pin = models.IntegerField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    logo = models.TextField()

    class Meta:
        db_table = 'organization'

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,)
    user_type = models.CharField(max_length=220)

    class Meta:
        db_table = 'organizationMember'

    def __str__(self):
        return self.user


class Catagory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None, blank=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="catagory/",
                              null=True, default=None, blank=True)

    class Meta:
        db_table = "catagory"

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,)

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.name


class Offer(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=22, decimal_places=16)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,)

    class Meta:
        db_table = "offer"

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    description = models.TextField(null=True, default=None, blank=True)
    price = models.FloatField()
    size = models.IntegerField(null=True, default=None, blank=True)
    color = models.CharField(max_length=50, null=True,
                             default=None, blank=True)
    image = models.ImageField(upload_to="Product/",
                              null=True, default=None, blank=True)
    status = models.BooleanField(default=True)
    highlighted = models.BooleanField(default=False)
    offer = models.ForeignKey(Offer,
                              on_delete=models.CASCADE,)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,)
    organization = models.ForeignKey(Organization,
                                     on_delete=models.CASCADE,)
    item_count = models.IntegerField()
    item_left = models.IntegerField()
    created = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Product_image/")
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "productImage"


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=10)
    email = models.EmailField(
        max_length=254, null=True, blank=True, default=None)
    address = models.TextField()
    pin = models.IntegerField()
    landmark = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    # type = models.CharField( max_length=50)
    geolocation = models.CharField(
        max_length=50, default=None, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "address"


class Highlight(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = "highlight"


class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = "cart"


class Whishlist(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = "whishlist"


class Card(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    card_no = models.CharField(max_length=16)
    card_name = models.CharField(max_length=100)

    class Meta:
        db_table = "card"


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    created = models.DateTimeField(auto_created=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    txn_id = models.CharField(max_length=220, unique=True)
    amount = models.FloatField()

    class Meta:
        db_table = "payment"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    delivary_date = models.DateTimeField(null=True, blank=True, default=None)
    payment_status = models.BooleanField(default=False)
    inv_number = models.IntegerField()
    total_amount = models.FloatField()
    shiping_charge = models.FloatField(null=True, blank=True, default=0)
    delivary_remarks = models.TextField(null=True, blank=True, default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "order"


class OrderDeatails(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    amount = models.FloatField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "orderDeatails"


class OrderTracker(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=220)
    description = models.CharField(max_length=220)
    current_loc = models.CharField(max_length=220)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = "orderTracker"


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    condent = models.TextField()
    date = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = "review"


class Rating(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = "rating"
