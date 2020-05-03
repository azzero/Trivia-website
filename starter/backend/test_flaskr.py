import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    #This class represents the trivia test case

    def setUp(self):
        #Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        #Executed after reach test
        pass

    
    #todo Write at least one test for each test for successful operation and for expected errors.
    
    def test_getting_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
    
    def test_404_requesting_beyond_categories_page(self):
        res=self.client().get("categories/2")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    # get questions test
    def test_get_paginated_questions(self):
        res=self.client().get("/questions?page=1")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))
    # wrong page test
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    #delete question test
    # def test_delete_question(self):
    #     res=self.client().delete("/questions/24")
    #     question=Question.query.filter(Question.id==24).one_or_none()
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(question,None)
    #delete wrong question test
    def test_422_delete_unexist_question(self):
        res=self.client().delete("/questions/1")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    #Add new question test 
    def test_create_new_question(self):
        res=self.client().post("/questions", json={"question":"question test","answer":"answer test ","difficulty":2,"category_value":"1"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
    #test : create new question not allowed
    def test_405_create_new_question_not_allowed(self):
        res=self.client().post("questions/12",json={"question":"question test","answer":"answer test ","difficulty":2,"category_value":"1"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"method not allowed")
    #test : search for question
    def test_search_for_question(self):
        res=self.client().post("/questions/search", json={"searchTerm":"a"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
    # test : searching not found 
    def test_404_searchig_not_found(self):
        res=self.client().post("questions/search/12",json={"searchTerm":"a"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")
    # test : get questions by category 
    def test_get_questions_by_category(self):
        res=self.client().get("/categories/1/questions")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
    #test : get questions by categories not found 
    def test_404_get_questions_by_category_not_found(self):
        res=self.client().get("/categories/1/questions/221")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"resource not found")
    #test : quizzes 
    def test_quezzies(self):
        res=self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"id":"2","type":"Art"}})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])
    # test : quizzes method not allowed 
    def test_405_quezzes_method_not_allowed(self):
        res=self.client().patch("/quizzes")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"method not allowed")
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()