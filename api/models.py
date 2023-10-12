from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=25)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=100)
    category=models.CharField(max_length=25)
    image=models.ImageField(null=True,blank=True,upload_to="images")

    # custom method for calculating avg rating
    # to act this custom method as a field we can decorate it with property
    @property
    def avg_rating(self):
        ratings=self.product_reviews.all().values_list("rating",flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0

    def __str__(self):
        return f'{self.name,(self.price),(self.category)}'


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_carts')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_carts')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username,self.product.name}'

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_reviews')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_reviews')
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product.name,self.rating,self.comment}'





class Author(models.Model):
    name = models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name="books")
    publication_date = models.DateField()
    countries = models.ManyToManyField(Country)
    is_bestselling=models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=1)

    def __str__(self):
        return self.title
