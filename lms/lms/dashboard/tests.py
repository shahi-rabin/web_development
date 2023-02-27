from django.test import TestCase

# Create your tests here.

from dashboard.models import *


from django.db import connections
from django.db.utils import OperationalError
db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    connected = False
else:
    connected = True

# Create your tests here.
class LogisticsDataModelTestcase(TestCase):
    @classmethod
    def setUpTestData(cls):
        LogisticsData.objects.create(studentId="101", bookName="Book1", borrowDate="1/2/2021", ReturnDate="1/2/2022")
	

    def test_bookname_method(self):
        student = LogisticsData.objects.get(id=1)        
        self.assertEqual(str(student.bookName))

    def test_date_method(self):
        student = LogisticsData.objects.get(id=1)        
        self.assertEqual(date(student.borrowDate))


class StudentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_students = 30
        for student_id in range(number_of_students):
            LogisticsData.objects.create(studentId="101", bookName="Book1", borrowDate="1/2/2021", ReturnDate="1/2/2022")

    def test_url_exists(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('students'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


def test_database_conn(self):
	logistics = LogisticsData.objects.all()
	self.assertTrue(len(logistics))


