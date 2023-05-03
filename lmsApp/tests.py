from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from lmsApp.models import Category, SubCategory, Books, Students, Borrow
from lmsApp.forms import SaveUser, UpdateProfile
from django.contrib.auth.models import User
from django.test import TestCase


class TestModels(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1', description='Category description')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Subcategory 1', description='Subcategory description')
        self.book = Books.objects.create(sub_category=self.subcategory, isbn='1234', title='Book 1', description='Book description', author='Author', publisher='Publisher', date_published=timezone.now())
        self.student = Students.objects.create(code='001', first_name='First', middle_name='Middle', last_name='Last', gender='Male', contact='1234567890', email='email@example.com', address='Address', department='Department')
        self.borrow = Borrow.objects.create(student=self.student, book=self.book, borrowing_date=datetime.now().date(), return_date=datetime.now().date() + timedelta(days=7))

    def test_category_model(self):
        self.assertEqual(str(self.category), 'Category 1')

    def test_subcategory_model(self):
        self.assertEqual(str(self.subcategory), 'Category 1 - Subcategory 1')

    def test_book_model(self):
        self.assertEqual(str(self.book), '1234 - Book 1')

    def test_student_model(self):
        self.assertEqual(str(self.student), '001 - First Middle Last')

    def test_borrow_model(self):
        self.assertEqual(str(self.borrow), '001')


class TestForms(TestCase):
    def test_save_user_form(self):
        form = SaveUser(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_update_profile_form_username_change(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form = UpdateProfile(instance=user, data={
            'email': 'test@example.com',
            'username': 'newtestuser',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertFalse(form.is_valid())

    def test_save_user_form_password_mismatch(self):
        form = SaveUser(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'mismatchedpassword'
        })
        self.assertFalse(form.is_valid())

    def test_save_user_form_missing_email(self):
        form = SaveUser(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    def test_update_profile_form_username_exists(self):
        existing_user = User.objects.create_user(username='existinguser', password='testpassword')
        user = User.objects.create_user(username='testuser', password='testpassword')
        form = UpdateProfile(instance=user, data={
            'email': 'test@example.com',
            'username': 'existinguser',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertFalse(form.is_valid())


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Fiction', description='Books of fictional stories')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_status_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_delete_flag_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('delete_flag').verbose_name
        self.assertEquals(field_label, 'delete flag')

    def test_date_added_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('date_added').verbose_name
        self.assertEquals(field_label, 'date added')

    def test_date_created_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_description_blank(self):
        category = Category.objects.get(id=1)
        blank = category._meta.get_field('description').blank
        self.assertEquals(blank, True)


    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.name}'
        self.assertEquals(expected_object_name, str(category))


class SubCategoryModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Fiction', description='Books of fictional stories')
        SubCategory.objects.create(category=category, name='Science Fiction', description='Books of science fiction stories')

    def test_category_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'category')

    def test_name_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_status_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_delete_flag_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('delete_flag').verbose_name
        self.assertEquals(field_label, 'delete flag')

    def test_date_added_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('date_added').verbose_name
        self.assertEquals(field_label, 'date added')

    def test_date_created_label(self):
        subcategory = SubCategory.objects.get(id=1)
        field_label = subcategory._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_name_max_length(self):
        subcategory = SubCategory.objects.get(id=1)
        max_length = subcategory._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_description_blank(self):
        subcategory = SubCategory.objects.get(id=1)
        blank = subcategory._meta.get_field('description').blank
        self.assertEquals(blank, True)

 
  