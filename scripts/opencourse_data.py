#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript courses profiles account.EmailAddress
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction


class BasicImportHelper(object):
    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(
        self,
        original_class,
        original_pk_name,
        the_class,
        pk_name,
        pk_value,
        obj_content,
    ):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = {pk_name: pk_value}
        the_obj = the_class.objects.get(**search_data)
        # print(the_obj)
        return the_obj

    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper

    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type(
        "DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper), {}
    )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if "import_helper" in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
    from dateutil.tz import tzoffset
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)


def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()


def import_data():
    # Initial Imports
    from django.contrib.auth.models import Group

    # Processing model: opencourse.profiles.models.User

    from opencourse.profiles.models import User

    profiles_user_1 = User()
    profiles_user_1.password = (
        "pbkdf2_sha256$180000$cwXsrztq2kJE$S0uNCeGQ+FvIIi/LlodoNOIBkurUaDpFLoPpstMEetA="
    )
    profiles_user_1.last_login = dateutil.parser.parse(
        "2020-05-10T20:46:18.956512+00:00"
    )
    profiles_user_1.is_superuser = False
    profiles_user_1.username = "professor@gmail.com"
    profiles_user_1.first_name = ""
    profiles_user_1.last_name = ""
    profiles_user_1.email = "professor@gmail.com"
    profiles_user_1.is_staff = False
    profiles_user_1.is_active = True
    profiles_user_1.date_joined = dateutil.parser.parse(
        "2020-05-10T20:19:13.787163+00:00"
    )
    profiles_user_1 = importer.save_or_locate(profiles_user_1)

    profiles_user_2 = User()
    profiles_user_2.password = (
        "pbkdf2_sha256$180000$jQbED5mRC3FC$rGHmLPbEnbCrOGGHpIxdbpEjAWH76Dj4auzItGjxy3Y="
    )
    profiles_user_2.last_login = dateutil.parser.parse(
        "2020-05-10T20:20:06.664503+00:00"
    )
    profiles_user_2.is_superuser = True
    profiles_user_2.username = "admin"
    profiles_user_2.first_name = ""
    profiles_user_2.last_name = ""
    profiles_user_2.email = "admin@gmail.com"
    profiles_user_2.is_staff = True
    profiles_user_2.is_active = True
    profiles_user_2.date_joined = dateutil.parser.parse(
        "2020-05-10T20:19:57.067332+00:00"
    )
    profiles_user_2 = importer.save_or_locate(profiles_user_2)

    profiles_user_3 = User()
    profiles_user_3.password = (
        "pbkdf2_sha256$180000$GPo9wAK6xKK7$NERotmMpKK7hKesccmfbreFEjUBtlB+iMk1n1lR/mvc="
    )
    profiles_user_3.last_login = dateutil.parser.parse(
        "2020-05-10T20:31:45.395920+00:00"
    )
    profiles_user_3.is_superuser = False
    profiles_user_3.username = "student@gmail.com"
    profiles_user_3.first_name = ""
    profiles_user_3.last_name = ""
    profiles_user_3.email = "student@gmail.com"
    profiles_user_3.is_staff = False
    profiles_user_3.is_active = True
    profiles_user_3.date_joined = dateutil.parser.parse(
        "2020-05-10T20:31:18.694372+00:00"
    )
    profiles_user_3 = importer.save_or_locate(profiles_user_3)

    # Processing model: opencourse.profiles.models.Student

    from opencourse.profiles.models import Student

    profiles_student_1 = Student()
    profiles_student_1.slug = "studentgmailcom"
    profiles_student_1.user = profiles_user_3
    profiles_student_1.picture = ""
    profiles_student_1.email_verified = False
    profiles_student_1.first_name_ar = None
    profiles_student_1.last_name_ar = None
    profiles_student_1.address = None
    profiles_student_1.city = None
    profiles_student_1.dob = None
    profiles_student_1.edulevel = None
    profiles_student_1.tel = ""
    profiles_student_1.whatsapp = None
    profiles_student_1.email = None
    profiles_student_1.dateadd = None
    profiles_student_1.contacts_requests = 0
    profiles_student_1 = importer.save_or_locate(profiles_student_1)

    # Processing model: opencourse.profiles.models.Professor

    from opencourse.profiles.models import Professor

    profiles_professor_1 = Professor()
    profiles_professor_1.slug = "professorgmailcom"
    profiles_professor_1.user = profiles_user_1
    profiles_professor_1.picture = ""
    profiles_professor_1.email_verified = False
    profiles_professor_1.first_name_ar = None
    profiles_professor_1.last_name_ar = None
    profiles_professor_1.address = None
    profiles_professor_1.city = None
    profiles_professor_1.dob = None
    profiles_professor_1.edulevel = None
    profiles_professor_1.tel = ""
    profiles_professor_1.whatsapp = None
    profiles_professor_1.email = None
    profiles_professor_1.dateadd = None
    profiles_professor_1.contacts_requests = 0
    profiles_professor_1.bio = None
    profiles_professor_1.yearsexperience = None
    profiles_professor_1.act_position = None
    profiles_professor_1.dateexpir = None
    profiles_professor_1.listed = None
    profiles_professor_1.feespaid = None
    profiles_professor_1 = importer.save_or_locate(profiles_professor_1)

    # Processing model: opencourse.profiles.models.Review

    from opencourse.profiles.models import Review

    profiles_review_1 = Review()
    profiles_review_1.professor = profiles_professor_1
    profiles_review_1.score = 5
    profiles_review_1.text = "Крутой курс, нравится"
    profiles_review_1.content_type = ContentType.objects.get(
        app_label="profiles", model="professor"
    )
    profiles_review_1.author_id = 1
    profiles_review_1 = importer.save_or_locate(profiles_review_1)

    profiles_review_2 = Review()
    profiles_review_2.professor = profiles_professor_1
    profiles_review_2.score = 5
    profiles_review_2.text = "Хороший курс"
    profiles_review_2.content_type = ContentType.objects.get(
        app_label="profiles", model="professor"
    )
    profiles_review_2.author_id = 1
    profiles_review_2 = importer.save_or_locate(profiles_review_2)

    profiles_review_3 = Review()
    profiles_review_3.professor = profiles_professor_1
    profiles_review_3.score = 2
    profiles_review_3.text = "bad course!"
    profiles_review_3.content_type = ContentType.objects.get(
        app_label="profiles", model="professor"
    )
    profiles_review_3.author_id = 1
    profiles_review_3 = importer.save_or_locate(profiles_review_3)

    # Processing model: allauth.account.models.EmailAddress

    from allauth.account.models import EmailAddress

    account_emailaddress_1 = EmailAddress()
    account_emailaddress_1.user = profiles_user_1
    account_emailaddress_1.email = "professor@gmail.com"
    account_emailaddress_1.verified = True
    account_emailaddress_1.primary = True
    account_emailaddress_1 = importer.save_or_locate(account_emailaddress_1)

    account_emailaddress_2 = EmailAddress()
    account_emailaddress_2.user = profiles_user_3
    account_emailaddress_2.email = "student@gmail.com"
    account_emailaddress_2.verified = True
    account_emailaddress_2.primary = True
    account_emailaddress_2 = importer.save_or_locate(account_emailaddress_2)

    # Processing model: opencourse.courses.models.Course

    from opencourse.courses.models import Course

    courses_course_1 = Course()
    courses_course_1.slug = "algebra-for-beginners"
    courses_course_1.professor = profiles_professor_1
    courses_course_1.city = courses_city_1
    courses_course_1.title = "Algebra for beginners"
    courses_course_1.title_ar = None
    courses_course_1.descrip = "Good course"
    courses_course_1.extrainfo = None
    courses_course_1.payactive = None
    courses_course_1.active = None
    courses_course_1.dateexp = None
    courses_course_1.starthostdate = None
    courses_course_1.endhostdate = None
    courses_course_1.hosted = None
    courses_course_1.hostactive = None
    courses_course_1.level = courses_courselevel_1
    courses_course_1.duration = courses_courseduration_1
    courses_course_1 = importer.save_or_locate(courses_course_1)

    courses_course_1.age.add(courses_courseage_1)
    courses_course_1.area.add(courses_coursearea_1)
    courses_course_1.language.add(courses_courselanguage_1)

    courses_course_2 = Course()
    courses_course_2.slug = "course"
    courses_course_2.professor = profiles_professor_1
    courses_course_2.city = courses_city_2
    courses_course_2.title = "Термодинамика"
    courses_course_2.title_ar = None
    courses_course_2.descrip = "Лучший курс."
    courses_course_2.extrainfo = None
    courses_course_2.payactive = None
    courses_course_2.active = None
    courses_course_2.dateexp = None
    courses_course_2.starthostdate = None
    courses_course_2.endhostdate = None
    courses_course_2.hosted = None
    courses_course_2.hostactive = None
    courses_course_2.level = courses_courselevel_1
    courses_course_2.duration = courses_courseduration_1
    courses_course_2 = importer.save_or_locate(courses_course_2)

    courses_course_2.age.add(courses_courseage_1)
    courses_course_2.area.add(courses_coursearea_2)
    courses_course_2.language.add(courses_courselanguage_7)

    # Processing model: opencourse.courses.models.CourseLocation

    from opencourse.courses.models import CourseLocation

    courses_courselocation_1 = CourseLocation()
    courses_courselocation_1.location_type = courses_courselocationtype_1
    courses_courselocation_1.course = courses_course_1
    courses_courselocation_1.description = None
    courses_courselocation_1.price = 1
    courses_courselocation_1.currency = courses_currency_1
    courses_courselocation_1.number_sessions = None
    courses_courselocation_1.coursestartdate = None
    courses_courselocation_1.courseenddate = None
    courses_courselocation_1 = importer.save_or_locate(courses_courselocation_1)

    courses_courselocation_2 = CourseLocation()
    courses_courselocation_2.location_type = courses_courselocationtype_1
    courses_courselocation_2.course = courses_course_2
    courses_courselocation_2.description = None
    courses_courselocation_2.price = 1
    courses_courselocation_2.currency = courses_currency_2
    courses_courselocation_2.number_sessions = None
    courses_courselocation_2.coursestartdate = None
    courses_courselocation_2.courseenddate = None
    courses_courselocation_2 = importer.save_or_locate(courses_courselocation_2)

    # Processing model: django.contrib.auth.models.Group

    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    professor_permission = Permission.objects.get(codename="access_professor_pages")
    students_permission = Permission.objects.get(codename="access_student_pages")

    auth_group_1 = Group()
    auth_group_1.name = 'Students'
    auth_group_1 = importer.save_or_locate(auth_group_1)

    auth_group_1.permissions.add(students_permission)

    auth_group_2 = Group()
    auth_group_2.name = 'Professors'
    auth_group_2 = importer.save_or_locate(auth_group_2)

    auth_group_2.permissions.add(professor_permission)
    auth_group_2.permissions.add(students_permission)

    # Re-processing model: opencourse.profiles.models.User

    profiles_user_1.groups.add(auth_group_2)
    profiles_user_3.groups.add(auth_group_1)
