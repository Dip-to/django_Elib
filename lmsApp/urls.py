from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home-page"),  # Home page
    path('login', views.login_page, name='login-page'),  # Login page
    path('register', views.userregister, name='register-page'),  # Register page
    path('save_register', views.save_register, name='register-user'),  # Save register page
    path('user_login', views.login_user, name='login-user'),  # User login page
    path('home', views.home, name='home-page'),  # Home page
    path('logout', views.logout_user, name='logout'),  # Logout page
    path('profile', views.profile, name='profile-page'),  # Profile page
    path('update_password', views.update_password, name='update-password'),  # Update password page
    path('update_profile', views.update_profile, name='update-profile'),  # Update profile page
    path('users', views.users, name='user-page'),  # Users page
    path('manage_user', views.manage_user, name='manage-user'),  # Manage user page
    path('manage_user/<int:pk>', views.manage_user, name='manage-user-pk'),  # Manage user with primary key
    path('save_user', views.save_user, name='save-user'),  # Save user page
    path('delete_user/<int:pk>', views.delete_user, name='delete-user'),  # Delete user with primary key
    path('category', views.category, name='category-page'),  # Category page
    path('manage_category', views.manage_category, name='manage-category'),  # Manage category page
    path('manage_category/<int:pk>', views.manage_category, name='manage-category-pk'),  # Manage category with primary key
    path('view_category/<int:pk>', views.view_category, name='view-category-pk'),  # View category with primary key
    path('save_category', views.save_category, name='save-category'),  # Save category page
    path('delete_category/<int:pk>', views.delete_category, name='delete-category'),  # Delete category with primary key
    path('sub_category', views.sub_category, name='sub_category-page'),  # Sub-category page
    path('manage_sub_category', views.manage_sub_category, name='manage-sub_category'),  # Manage sub-category page
    path('manage_sub_category/<int:pk>', views.manage_sub_category, name='manage-sub_category-pk'),  # Manage sub-category with primary key
    path('view_sub_category/<int:pk>', views.view_sub_category, name='view-sub_category-pk'),  # View sub-category with primary key
    path('save_sub_category', views.save_sub_category, name='save-sub_category'),  # Save sub-category page
    path('delete_sub_category/<int:pk>', views.delete_sub_category, name='delete-sub_category'),  # Delete sub-category with primary key
    path('books', views.books, name='book-page'),  # Book page
    path('manage_book', views.manage_book, name='manage-book'),  # Manage book page
    path('manage_book/<int:pk>', views.manage_book, name='manage-book-pk'),  # Manage book with primary key
    path('view_book/<int:pk>', views.view_book, name='view-book-pk'),  # View book with primary key
    path('save_book', views.save_book, name='save-book'),  # Save book page
    path('delete_book/<int:pk>', views.delete_book, name='delete-book'),  # Delete book with primary key
    path('students', views.students, name='student-page'),  # Students page
    path('manage_student', views.manage_student, name='manage-student'),  # Manage student page
    path('manage_student/<int:pk>', views.manage_student, name='manage-student-pk'),  # Manage student with primary key
    path('view_student/<int:pk>', views.view_student, name='view-student-pk'),  # View student with primary key
    path('save_student', views.save_student, name='save-student'),  # Save student page
    path('delete_student/<int:pk>', views.delete_student, name='delete-student'),  # Delete student with primary key
    path('borrows', views.borrows, name='borrow-page'),  # Borrows page
    path('manage_borrow', views.manage_borrow, name='manage-borrow'),  # Manage borrow page
    path('manage_borrow/<int:pk>', views.manage_borrow, name='manage-borrow-pk'),  # Manage borrow with primary key
    path('view_borrow/<int:pk>', views.view_borrow, name='view-borrow-pk'),  # View borrow with primary key
    path('save_borrow', views.save_borrow, name='save-borrow'),  # Save borrow page
    path('delete_borrow/<int:pk>', views.delete_borrow, name='delete-borrow'),  # Delete borrow with primary key
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
