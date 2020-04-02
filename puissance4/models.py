from django.db import models

# Create your models here.


from django.db.models import CharField, Model, PositiveSmallIntegerField, BooleanField

class Game(Model):
    case00 = PositiveSmallIntegerField(default=0)
    case01 = PositiveSmallIntegerField(default=0)
    case02 = PositiveSmallIntegerField(default=0)
    case03 = PositiveSmallIntegerField(default=0)
    case04 = PositiveSmallIntegerField(default=0)
    case05 = PositiveSmallIntegerField(default=0)
    case06 = PositiveSmallIntegerField(default=0)
    case00 = PositiveSmallIntegerField(default=0)
    case01 = PositiveSmallIntegerField(default=0)
    case02 = PositiveSmallIntegerField(default=0)
    case03 = PositiveSmallIntegerField(default=0)
    case04 = PositiveSmallIntegerField(default=0)
    case05 = PositiveSmallIntegerField(default=0)
    case06 = PositiveSmallIntegerField(default=0)
    case10 = PositiveSmallIntegerField(default=0)
    case11 = PositiveSmallIntegerField(default=0)
    case12 = PositiveSmallIntegerField(default=0)
    case13 = PositiveSmallIntegerField(default=0)
    case14 = PositiveSmallIntegerField(default=0)
    case15 = PositiveSmallIntegerField(default=0)
    case16 = PositiveSmallIntegerField(default=0)
    case20 = PositiveSmallIntegerField(default=0)
    case21 = PositiveSmallIntegerField(default=0)
    case22 = PositiveSmallIntegerField(default=0)
    case23 = PositiveSmallIntegerField(default=0)
    case24 = PositiveSmallIntegerField(default=0)
    case25 = PositiveSmallIntegerField(default=0)
    case26 = PositiveSmallIntegerField(default=0)
    case30 = PositiveSmallIntegerField(default=0)
    case31 = PositiveSmallIntegerField(default=0)
    case32 = PositiveSmallIntegerField(default=0)
    case33 = PositiveSmallIntegerField(default=0)
    case34 = PositiveSmallIntegerField(default=0)
    case35 = PositiveSmallIntegerField(default=0)
    case36 = PositiveSmallIntegerField(default=0)
    case40 = PositiveSmallIntegerField(default=0)
    case41 = PositiveSmallIntegerField(default=0)
    case42 = PositiveSmallIntegerField(default=0)
    case43 = PositiveSmallIntegerField(default=0)
    case44 = PositiveSmallIntegerField(default=0)
    case45 = PositiveSmallIntegerField(default=0)
    case46 = PositiveSmallIntegerField(default=0)
    case50 = PositiveSmallIntegerField(default=0)
    case51 = PositiveSmallIntegerField(default=0)
    case52 = PositiveSmallIntegerField(default=0)
    case53 = PositiveSmallIntegerField(default=0)
    case54 = PositiveSmallIntegerField(default=0)
    case55 = PositiveSmallIntegerField(default=0)
    case56 = PositiveSmallIntegerField(default=0)
    turn = PositiveSmallIntegerField(default=1)
    fini = BooleanField(default=False)
    def get(self, i,j):
        return self.__dict__['case'+str(i)+str(j)]
    def set(self, i,j,k):
        self.__dict__['case'+str(i)+str(j)] = k