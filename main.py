import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    age = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<h1>Main Page</h1>')

class AboutPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to my site\'s about page!')

class SuccessPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Success! <a href="/student/list">view students</a>')

class CreateStudentPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create_student_page.html')
        self.response.write(template.render())

    def post(self):
        student = Student()
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.age = int(self.request.get('age'))
        student.put()
        self.redirect('/success')

class StudentListPage(webapp2.RequestHandler):
    def get(self):
        students = Student.query().order(-Student.date).fetch()
        logging.info(students)
        template_data = {
            'student_list': students
        }
        template = JINJA_ENVIRONMENT.get_template('student_list_page.html')
        self.response.write(template.render(template_data))

class  StudentEdit(webapp2.RequestHandler):
    def get(self,student_id):
        student = Student.get_by_id(int(student_id))
        template_data = {
            'student': student
        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))

    def post(self,student_id):
        student = Student.get_by_id(int(student_id))
        student.first_name = self.request.get('newFirstName')
        student.last_name = self.request.get('newLastName')
        student.age = int(self.request.get('newAge'))
        student.put()
        self.redirect('/success')

class  StudentDelete(webapp2.RequestHandler):
    def get(self,student_id):
        student = Student.get_by_id(int(student_id))
        student.key.delete()
        self.redirect('/success')

app = webapp2.WSGIApplication([
    ('/student/create', CreateStudentPage),
    ('/student/list', StudentListPage),
    ('/about', AboutPage),
    ('/success', SuccessPage),
    ('/home', MainPage),
    ('/', MainPage),
    ('/student/edit/(.*)', StudentEdit),
    ('/student/delete/(.*)', StudentDelete)
], debug=True)