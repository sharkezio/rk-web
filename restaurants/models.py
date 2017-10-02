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
    # def get_queryset(self):
    #     return super(FoodManager, self).get_queryset().filter(
    #         is_spicy=True)

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
        # total = 10
        return int(total)

    # def this_user_up_vote(self):
    #     thisUserUpVote = self.userUpVotes.filter(
    #         id=self.request.user.id).count()
    #     print "this_user_up_vote = ", thisUserUpVote
    #     return int(thisUserUpVote)

    # def this_user_down_vote(self):
    #     thisUserDownVote = self.userDownVotes.filter(
    #         id=self.request.user.id).count()
    #     print "this_user_down_vote = ", thisUserDownVote
    #     return int(thisUserDownVote)

    class Meta:
        # ordering = ['date_time']
        ordering = ['id']
        permissions = (
            ("can_comment", "Can comment"),
        )

# class Thread(models.Model):
#     # ...
#     userUpVotes = models.ManyToManyField(
#         User, blank=True, related_name='threadUpVotes')
#     userDownVotes = models.ManyToManyField(
#         User, blank=True, related_name='threadDownVotes')
