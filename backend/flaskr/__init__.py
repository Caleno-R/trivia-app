import datetime
import os
import sys
from tkinter import NO
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
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
                'categories': categories_formatted,
                'current_category': None

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

    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        # Get data from the request body
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        try:
            # Search for case insensitive strings
            search_results = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))
            )
            questions_formatted = [question.format()
                                   for question in search_results]

            return jsonify({
                'success': True,
                'SearchTerm': questions_formatted,
                'current_category': None,
                'total_questions': len(search_results.all())
            })
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def question_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            questions_formatted = [question.format() for question in questions]

            return jsonify({
                'succeed': True,
                'questions': questions_formatted,
                'current_categories': category_id,
                'total_questions': len(questions),
            })
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            # Get data from the request body
            body = request.get_json()
            category: Category = body.get('quiz_category', None)
            previous_questions_id: list[int] = body.get(
                'previous_questions', None)
            is_not_randomQuestion: bool = True
            while is_not_randomQuestion:
                all_question_ids = [
                    question.id for question in Question.query.all()]
                random_question_id: int = random.choice(all_question_ids)
                if random_question_id not in previous_questions_id:
                    random_question: Question = Question.query.get(
                        random_question_id)
                    if int(category['id']) == 0:
                        is_not_randomQuestion == False
                    if random_question.category == int(category['id']):
                        is_not_randomQuestion = False

            return jsonify({
                'success': True,
                'previousQuestions': previous_questions_id,
                'question': {
                    'question': random_question.question,
                    'answer': random_question.answer,
                    'category': random_question.category,
                    'difficulty': random_question.difficulty
                }
            })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

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
