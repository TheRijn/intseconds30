import binascii
import os
from random import randint, shuffle

from django.db import models
# Create your models here.
from django.db.models import Max


class Card(models.Model):
    number = models.fields.IntegerField(primary_key=True)

    def __str__(self):
        return f"Card {self.number} ({self.words.count()}): {', '.join(self.words_list)}"

    @property
    def words_list(self):
        return list(self.words.all().values_list('title', flat=True))

    @property
    def words_list_shuffled(self):
        words = self.words_list
        shuffle(words)
        return words

    def json(self):
        return {'card': self.number, 'words': self.words_list_shuffled}

    @staticmethod
    def random():
        max_number = Card.objects.all().aggregate(max_id=Max("number"))['max_id']
        while True:
            pk = randint(1, max_number)
            card = Card.objects.get(number=pk)
            if card:
                return card


class Word(models.Model):
    title = models.fields.CharField(max_length=50)
    card = models.ForeignKey(
        Card,
        related_name="words",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.title}"


def random_secret() -> str:
    return binascii.b2a_hex(os.urandom(8)).decode()


class Session(models.Model):
    last_activity = models.fields.DateTimeField(auto_now=True)
    started = models.fields.DateTimeField(auto_now_add=True)

    secret = models.fields.CharField(max_length=16, default=random_secret)
    used_cards = models.ManyToManyField(Card, blank=True)
