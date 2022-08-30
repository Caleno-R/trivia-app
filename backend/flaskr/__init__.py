import datetime
import os
import sys
from tkinter import NO
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions_formatted = [question.format() for question in selection]
    current_questions = questions_formatted[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,DELETE,OPTIONS')

        return response

    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.type).all()

            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in categories}

            })
        except Exception as e:
            abort(404)

    @app.route('/questions')
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()

            current_questions = paginate_questions(request, selection)
            categories_formatted = {
                category.id: category.type for category in categories}

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': None,
                'categories': categories_formatted

            })
        except Exception as e:
            print(sys.exc_info())
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():

        # Get data from the request body
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer_text = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            # Create question
            question = Question(
                question=new_question,
                answer=new_answer_text,
                category=new_category,
                difficulty=new_difficulty)

            # Update to db
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })
        except:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_questions():

        # Get data from the request body
        body = request.get_json()

        search_term = body.get('search', None)

        try:
            if search_term:

                # Search for case insensitive strings
                search_results = Question.query.order_by(Question.id).filter(
                    Question.title.ilike('%{}%'.format(search_term))
                )
                questions_formatted = [search_results.format()
                                       for question in search_results]

                return jsonify({
                    'success': True,
                    'questions': questions_formatted,
                    'current_category': None,
                    'total_questions': len(search_results.all())

                })
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400    


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404
    
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 422

    


    return app
