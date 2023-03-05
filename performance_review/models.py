import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# from ckeditor.fields import RichTextField


class Employee(models.Model):
    EMP_GENDER = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    EMP_RANKS = (
        ('CEO', 'Chief Executive Officer'),
        ('DIR', 'Director'),
        ('MAN', 'Manager'),
        ('WOR', 'Worker'),
        ('OTH', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='emp/profiles/', null=True, blank=True)
    gender = models.CharField(max_length=1, default='m', null=False, blank=False, choices=EMP_GENDER)
    contact_no = models.CharField(
        max_length=18, null=True, blank=True, help_text='employee phone or landline number'
    )
    address = models.TextField(
        null=True, blank=True, help_text='Complete address within area/street, city state and country etc.'
    )
    nic = models.CharField(max_length=50, null=True, blank=True, help_text='National Identification Card or ID card')
    org_id = models.CharField(max_length=50, null=True, blank=True,
                              help_text='Organizational Registration Number or ID')
    rank = models.CharField(
        max_length=3, null=True, blank=True, choices=EMP_RANKS,
        help_text='Employee Rank/Post/Destination within organization'
    )
    date_of_birth = models.DateTimeField(null=True, blank=True, help_text='Date of Birth - Format must be YYYY-MM-DD')
    joined_on = models.DateTimeField(null=True, blank=True, help_text='Date of Joining - Format must be YYYY-MM-DD')
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.pk} {self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.TextField(
        max_length=1000, null=False, blank=False, help_text='small description of this task 25-100 characters'
    )
    is_active = models.BooleanField(
        null=False, blank=False, default=True,
        help_text='If you check this it means the task is active and if you disable it it will be removed temporary'
    )
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.pk} {self.employee} "

    def save(self, *args, **kwargs):
        self.slug = slugify(self.employee)
        super(Review, self).save(*args, **kwargs)
