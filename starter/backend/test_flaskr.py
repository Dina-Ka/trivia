import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sys
from flaskr import create_app
from models import *
from sqlalchemy import func

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path ="postgresql://postgres:scholarship@localhost:5432/trivia"

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_categoty_retrival_200(self):
        response   = self.client().get('/categories')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertTrue(len(result['categories']))
        self.assertTrue(result['categories'])

    def test_categoty_retrival_404(self):
        response = self.client().get('/categories/D9i9n9a')
        result = json.loads(response.data)
        self.assertEqual(result['error'], 404)
        self.assertEqual(result['success'], False)



    def test_questions_retrival_200(self):
        response = self.client().get('/questions')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertTrue(len(result['questions']))
        self.assertTrue(result['categories'])

    def test_questions_retrival_404(self):
        response = self.client().get('/questions?page=100000000000000000000000000')
        result = json.loads(response.data)
        self.assertEqual(result['error'], 404)
        self.assertEqual(result['success'], False)

    # success
    def test_question_deletion(self):
        response = self.client().delete('/questions/4')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)

    # 422
    def test_question_deletion_422(self):
        response = self.client().delete('/questions/dina')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result['success'], False)

    # check insertion
    def test_question_addition_200(self):
        questionData = {
            "answer":"answer test",
            "category": '5',
            "difficulty": '1',
            "question": 'question test test'
        }
        # getTotalnumberofQuestions
        questions = Question.query.all()
        totalQuestions = [eachquestion.format() for eachquestion in questions]
        totalQuestionsLength = len(totalQuestions)
        totalQuestionsLength = totalQuestionsLength+1
        response = self.client().post('/questions',json=questionData)
        result = json.loads(response.data)
        print(result['total_questions'])
        print(totalQuestionsLength)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        # lastId
        self.assertEqual(result['total_questions'], totalQuestionsLength)

    # check insertion
    def test_question_addition_422(self):
        questionData = {
            "answer":"answer test",
            "category": '5',
            "difficulty": '1',
        }
        response = self.client().post('/questions', json=questionData)
        result = json.loads(response.data)
        self.assertEqual(result['error'], 422)
        self.assertEqual(result['success'], False)


   # check insertion
    def test_question_searchbox(self):
        searchTerm = {
            "searchTerm":'tItle'
        }
        response = self.client().post('/questions/searching', json=searchTerm)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)

        # check insertion

    def test_question_searchbox_404(self):
        searchTerm = {
            "searchTerm": ''
        }
        response = self.client().post('/questions/searching', json=searchTerm)
        result = json.loads(response.data)
        self.assertEqual(result['error'], 404)
        self.assertEqual(result['success'], False)

    def test_retrieving_Category_on_Click(self):
        response = self.client().get('/categories/2/questions')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertTrue(result['questions'])

    def test_retrieving_Category_on_Click_404(self):
        response = self.client().get('/categories/25/questions')
        result = json.loads(response.data)
        self.assertEqual(result['error'], 404)
        self.assertEqual(result['success'], False)



    def test_quiz_retrival(self):
        quizData = {
            "previous_questions": [],
            "quiz_category": {
                "id": '1',
                "type": 'Art'
            }
        }
        response = self.client().post('/quizzes', json=quizData)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertTrue(result['question'])

    def test_quiz_retrival_422(self):
        quizData = {
            "previous_questions": []
        }
        response = self.client().post('/quizzes', json=quizData)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result['success'], False)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()