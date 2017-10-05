from django.db import models
from django.db import connection

from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


class FoodManager(models.Manager):

    def sfood_order_by_price(self):
        return self.filter(is_spicy=True).order_by('price')

    def cheap_food_num(self):
        return self.filter(price__lte=100).count()

    def get_120_food(self):  # use SQL to get DATA.
                            # Need to import connection from django.db
        cursor = connection.cursor()
        cursor.execute("""
            SELECT name
            FROM restaurants_food
            WHERE price=120
        """)
        return [result[0] for result in cursor.fetchall()]


class SpicyFoodManager(models.Manager):
    def get_queryset(self):
        return super(SpicyFoodManager, self).get_queryset(
        ).filter(is_spicy=True)


class NotSpicyFoodManager(models.Manager):
    def get_queryset(self):
        return super(NotSpicyFoodManager, self).get_queryset(
        ).filter(is_spicy=False)


class Food(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    comment = models.CharField(max_length=50, blank=True)
    is_spicy = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant)
    objects = FoodManager()
    s_objects = SpicyFoodManager()
    ns_objects = NotSpicyFoodManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['price']


class Comment(models.Model):
    content = models.CharField(max_length=255)
    visitor = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_time = models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant)

    userUpVotes = models.ManyToManyField(
        User, blank=True, related_name='threadUpVotes')
    userDownVotes = models.ManyToManyField(
        User, blank=True, related_name='threadDownVotes')

    thisUserUpVote = models.BooleanField(default=False)
    thisUserDownVote = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

    def get_total_votes(self):
        total = self.userUpVotes.count() - self.userDownVotes.count()
        return int(total)

    class Meta:
        ordering = ['id']
        permissions = (
            ("can_comment", "Can comment"),
        )
