from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager

# Category model represents a book category
class Category(models.Model):
    name = models.CharField(max_length=250)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the category
    delete_flag = models.IntegerField(default=0)  # Delete flag for soft deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the category was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the category was created

    class Meta:
        verbose_name_plural = "List of Categories"

    def __str__(self):
        return str(f"{self.name}")


# SubCategory model represents a book subcategory, associated with a Category
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category associated with the subcategory
    name = models.CharField(max_length=250)  # Name of the subcategory
    description = models.TextField(blank=True, null=True)  # Optional description of the subcategory
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the subcategory
    delete_flag = models.IntegerField(default=0)  # Delete flag for soft deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the subcategory was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the subcategory was created

    class Meta:
        verbose_name_plural = "List of Categories"

    def __str__(self):
        return str(f"{self.category} - {self.name}")


# Books model represents a book, associated with a SubCategory
class Books(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)  # Subcategory associated with the book
    isbn = models.CharField(max_length=250)  # ISBN number of the book
    title = models.CharField(max_length=250)  # Title of the book
    description = models.TextField(blank=True, null=True)  # Optional description of the book
    author = models.TextField(blank=True, null=True)  # Author of the book
    publisher = models.CharField(max_length=250)  # Publisher of the book
    date_published = models.DateTimeField()  # Date when the book was published
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the book
    delete_flag = models.IntegerField(default=0)  # Delete flag for soft deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the book was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the book was created

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return str(f"{self.isbn} - {self.title}")


# Students model represents a student/member
class Students(models.Model):
    code = models.CharField(max_length=250, null=True)  # Code/identifier for the student
    first_name = models.CharField(max_length=250)  # First name of the student
    middle_name = models.CharField(max_length=250, blank=True, null=True)  # Middle name of the student (optional)
    last_name = models.CharField(max_length=250)  # Last name of the student
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')  # Gender of the student
    contact = models.CharField(max_length=250)  # Contact number of the student
    email = models.CharField(max_length=250)  # Email address of the student
    address = models.CharField(max_length=250)  # Address of the student
    department = models.CharField(max_length=250, blank=True, null=True)  # Department of the student (optional)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the student
    delete_flag = models.IntegerField(default=0)  # Delete flag for soft deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the student was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the student was created

    class Meta:
        verbose_name_plural = "List of Members"

    def __str__(self):
        return str(f"{self.code} - {self.first_name}{' ' + self.middle_name if not self.middle_name == '' else ''} {self.last_name}")

    def name(self):
        return str(f"{self.first_name}{' ' + self.middle_name if not self.middle_name == '' else ''} {self.last_name}")


# Borrow model represents a borrowing transaction
class Borrow(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_id_fk")  # Student/member associated with the borrowing transaction
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_id_fk")  # Book associated with the borrowing transaction
    borrowing_date = models.DateField()  # Date when the book was borrowed
    return_date = models.DateField()  # Date when the book is expected to be returned
    status = models.CharField(max_length=2, choices=(('1', 'Pending'), ('2', 'Returned')), default=1)  # Status of the borrowing transaction
    date_added = models.DateTimeField(default=timezone.now)  # Date when the borrowing transaction was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the borrowing transaction was created

    class Meta:
        verbose_name_plural = "Borrowing Transactions"

    def __str__(self):
        return str(f"{self.student.code}")

