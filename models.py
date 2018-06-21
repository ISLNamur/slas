from django.db import models

from core.models import StudentLDAP


class Activity(models.Model):
    name = models.CharField(max_length=200)
    animator = models.CharField(max_length=200)
    description = models.CharField(max_length=5000, blank=True)
    day = models.CharField(max_length=100)
    slot = models.BooleanField()
    is_free = models.BooleanField(default=False)
    age = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return "%s | %s [%i]" % (self.name, self.day, int(self.slot))


class ActivityInscription(models.Model):
    activity = models.ForeignKey(Activity)
    student_first_name = models.CharField(max_length=200)
    student_surname = models.CharField(max_length=200)
    classe = models.CharField(max_length=200)
    birth = models.DateField("birth")
    resp_first_name = models.CharField(max_length=200)
    resp_surname = models.CharField(max_length=200)
    resp_address = models.CharField(max_length=400)
    resp_email = models.EmailField()
    resp_email_2 = models.EmailField(null=True, blank=True)
    resp_telephone = models.CharField(max_length=200)
    resp_telephone_2 = models.CharField(max_length=200)
    datetime_inscription = models.DateTimeField("Creation date")
    answered = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    student = models.ForeignKey(StudentLDAP, default=None, blank=True, null=True)
