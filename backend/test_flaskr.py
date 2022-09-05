import os
import unittest
import json
import pytest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
       
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_user = 'postgres'
        self.database_password = 'password'
        self.database_host = 'localhost'
        self.database_port = '5432'
        self.database_path = 'postgresql://{}:{}@{}:{}/{}'.format(
            self.database_user,
            self.database_password,
            self.database_host,
            self.database_port,
            self.database_name
        )
        self.new_question = {
            'id': 24,
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 1,
            'category': 2,
        }
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

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)

    def test_404_sent_requesting_non_existing_category(self):
        res = self.client().get('/categories/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_retrieve_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 10)
        # self.assertEqual(data['total_questions'], 52)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(data['current_category'], None)

    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 175)

    def test_delete_question(self):
        #  change for final test
        res = self.client().delete('/questions/38') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 38)

    def test_search_questions(self):
        res = self.client().post(
            '/questions/search',
            json={'searchTerm': 'Clay'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['SearchTerm'])
        self.assertIsNotNone(data['total_questions'])
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], None)

    def test_search_questions_without_results(self):
        res = self.client().post(
            '/search',
            json={'searchTerm': 'safari'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['succeed'], True)

        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)
        # self.assertEqual(len(data['questions']), 135)
        # self.assertEqual(data['total_questions'], 135)
        self.assertEqual(data['current_categories'], 2)

    def test_quizzes_with_category_and_without_previous_questions(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {
                'id': '3',
                'type': 'Geography'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertIsInstance(data['question'], dict)

    def test_quizzes_with_category_and_with_some_previous_questions(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertIsInstance(data['question'], dict)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
