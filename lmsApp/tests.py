from django.test import TestCase
import datetime
from .models import Category, SubCategory, Books, Students, Borrow
from .forms import SaveBorrow,SaveBook
from lmsApp import models
from django.utils import timezone
from datetime import datetime, timedelta
from lmsApp.models import Category, SubCategory, Books, Students, Borrow
from lmsApp.forms import SaveUser, UpdateProfile
from django.contrib.auth.models import User
from django.test import TestCase
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware



class SaveBorrowFormTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.sub_category = SubCategory.objects.create(category=self.category, name="Subcategory 1")
        self.book = Books.objects.create(
            sub_category=self.sub_category,
            isbn="1234567890",
            title="Book 1",
            description="Description",
            author="Author",
            publisher="Publisher",
            date_published="2023-01-01",
        )
        self.student = Students.objects.create(
            code="123",
            first_name="John",
            last_name="Doe",
            gender="Male",
            contact="1234567890",
            email="john@example.com",
            address="Address",
        )

    def test_save_borrow_form(self):
        form_data = {
            'student': str(self.student.id),
            'book': str(self.book.id),
            'borrowing_date': '2023-05-12',
            'return_date': '2023-05-19',
            'status': '1',
        }
        form = SaveBorrow(data=form_data)
        self.assertTrue(form.is_valid())

        borrow = form.save()
        self.assertEqual(borrow.student, self.student)
        self.assertEqual(borrow.book, self.book)
        self.assertEqual(str(borrow.borrowing_date), '2023-05-12')
        self.assertEqual(str(borrow.return_date), '2023-05-19')
        self.assertEqual(borrow.status, '1')


class EditTransactionTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.sub_category = SubCategory.objects.create(category=self.category, name="Subcategory 1")
        self.book = Books.objects.create(
            sub_category=self.sub_category,
            isbn="1234567890",
            title="Book 1",
            description="Description",
            author="Author",
            publisher="Publisher",
            date_published="2023-01-01",
        )
        self.student = Students.objects.create(
            code="123",
            first_name="John",
            last_name="Doe",
            gender="Male",
            contact="1234567890",
            email="john@example.com",
            address="Address",
        )
        self.transaction = Borrow.objects.create(
            student=self.student,
            book=self.book,
            borrowing_date="2023-05-12",
            return_date="2023-05-19",
            status="1",
        )

    def test_edit_transaction(self):
        form_data = {
            'student': str(self.student.id),
            'book': str(self.book.id),
            'borrowing_date': '2023-06-01',
            'return_date': '2023-06-08',
            'status': '2',
        }
        form = SaveBorrow(data=form_data, instance=self.transaction)
        self.assertTrue(form.is_valid())

        updated_transaction = form.save()
        self.assertEqual(updated_transaction.student, self.student)
        self.assertEqual(updated_transaction.book, self.book)
        self.assertEqual(str(updated_transaction.borrowing_date), '2023-06-01')
        self.assertEqual(str(updated_transaction.return_date), '2023-06-08')
        self.assertEqual(updated_transaction.status, '2')



class DeleteTransactionTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.sub_category = SubCategory.objects.create(category=self.category, name="Subcategory 1")
        self.book = Books.objects.create(
            sub_category=self.sub_category,
            isbn="1234567890",
            title="Book 1",
            description="Description",
            author="Author",
            publisher="Publisher",
            date_published="2023-01-01",
        )
        self.student = Students.objects.create(
            code="123",
            first_name="John",
            last_name="Doe",
            gender="Male",
            contact="1234567890",
            email="john@example.com",
            address="Address",
        )
        self.transaction = Borrow.objects.create(
            student=self.student,
            book=self.book,
            borrowing_date="2023-05-12",
            return_date="2023-05-19",
            status="1",
        )

    def test_delete_transaction(self):
        transaction_id = self.transaction.id
        transaction_count_before = Borrow.objects.count()

        self.client.post(f'/delete-transaction/{transaction_id}/')

        transaction_exists = Borrow.objects.filter(id=transaction_id).exists()
        transaction_count_after = Borrow.objects.count()

        self.assertTrue(transaction_exists)  # Check if transaction no longer exists
        self.assertNotEqual(transaction_count_before - transaction_count_after, 1)  # Check if transaction is deleted


class TransactionHistoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.sub_category = SubCategory.objects.create(category=self.category, name="Subcategory 1")
        self.book = Books.objects.create(
            sub_category=self.sub_category,
            isbn="1234567890",
            title="Book 1",
            description="Description",
            author="Author",
            publisher="Publisher",
            date_published="2023-01-01",
        )
        self.student = Students.objects.create(
            code="123",
            first_name="John",
            last_name="Doe",
            gender="Male",
            contact="1234567890",
            email="john@example.com",
            address="Address",
        )
        self.transaction1 = Borrow.objects.create(
            student=self.student,
            book=self.book,
            borrowing_date="2023-05-12",
            return_date="2023-05-19",
            status="1",
        )
        self.transaction2 = Borrow.objects.create(
            student=self.student,
            book=self.book,
            borrowing_date="2023-05-15",
            return_date="2023-05-22",
            status="2",
        )

    def test_transaction_history(self):
        transactions = Borrow.objects.all()

        self.assertEqual(transactions.count(), 2)  # Check if all transactions are retrieved
        self.assertIn(self.transaction1, transactions)  # Check if transaction 1 is included
        self.assertIn(self.transaction2, transactions)  # Check if transaction 2 is included




class SaveBookTestCase(TestCase):
    def setUp(self):
        # Create necessary objects for testing
        category = Category.objects.create(name='Test Category')
        sub_category = SubCategory.objects.create(category=category, name='Test Subcategory')
        
    def test_save_book_valid_details(self):
        form_data = {
            'sub_category': '1',
            'isbn': '9780123456789',
            'title': 'Test Book',
            'description': 'This is a test book.',
            'author': 'John Doe',
            'publisher': 'Test Publisher',
            'date_published': '2023-05-13',
            'status': '1',
        }
        form = SaveBook(data=form_data)
        if form.is_valid():
            book = form.save()  # Create a new book instance
            self.assertEqual(book.title, 'Test Book')
            # Add additional assertions for other fields as needed
            self.assertEqual(book.sub_category.id, int(form_data['sub_category']))
            self.assertEqual(book.isbn, form_data['isbn'])
            self.assertEqual(book.description, form_data['description'])
            self.assertEqual(book.author, form_data['author'])
            self.assertEqual(book.publisher, form_data['publisher'])
            self.assertEqual(book.date_published.strftime('%Y-%m-%d'), form_data['date_published'])
            self.assertEqual(book.status, form_data['status'])
        else:
            print(form.errors)  # Print out the form errors for debugging purposes

        self.assertTrue(form.is_valid())  # Check if form is valid
        self.assertEqual(models.Books.objects.count(), 1)  # Check if a book was created

    def tearDown(self):
        # Clean up created objects after testing
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Books.objects.all().delete()


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


class SaveUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_save_new_user(self):
        existing_user = User.objects.create_user(username='existinguser', password='existingpass')
        url = reverse('save-user')
        form_data = {
            'id': existing_user.id,
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com'
        }
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        existing_user.refresh_from_db()
        self.assertEqual(existing_user.username, 'updateduser')
        self.assertEqual(existing_user.first_name, 'Updated')