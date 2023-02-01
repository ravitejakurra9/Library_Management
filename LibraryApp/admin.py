from django.contrib import admin

from LibraryApp.models import Course, Book, Student, Issue_Book

# Register your models here.
admin.site.register(Course)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Issue_Book)