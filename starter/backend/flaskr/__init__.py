import os
from flask import Flask, request, abort, jsonify,flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import *
from sqlalchemy import desc, asc

# Number of Question per page
QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)
    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request_function(result):
        result.headers.add('Access-Control-Allow-Methods', 'PATCH,GET,POST,DELETE,OPTIONS,PUT')
        result.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        return result
    '''
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def categoty_retrival():
        # Get all categories
        try:
            allcategories = Category.query.filter().order_by(asc(Category.id))
            totalcategories = {}
            for category in allcategories:
                totalcategories[category.id] = category.type

            if len(totalcategories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': totalcategories
            })
        except:
            abort(404)


    '''
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route("/questions", methods=['GET'])
    def questions_retrival():
        # If the key doesnot exist it will be specified to one as a default value
        pageNumbers = request.args.get('page', 1, type=int)
        # print(pageNumbers)
        # define the end the start point in paginition
        startingPoint = (pageNumbers - 1) * QUESTIONS_PER_PAGE
        endingPoint = startingPoint + QUESTIONS_PER_PAGE

        # ***** Questions Retriving *****
        allQuestions = Question.query.filter().order_by(asc(Question.id))
        totalQuestions = [eachquestion.format() for eachquestion in allQuestions]

        # *****totalQuestions****
        if len(totalQuestions):
            lengthQuestions = len(totalQuestions)
        else:
            abort(404)
            lengthQuestions = 0

        totalQuestions = totalQuestions[startingPoint:endingPoint]
        if not len(totalQuestions):
            abort(404)

        # Get all categories
        allcategories = Category.query.filter().order_by(asc(Category.id))
        totalcategories = {}
        for category in allcategories:
            totalcategories[category.id] = category.type

        # Get categories "current category"
        current_category = []
        for question in totalQuestions:
            current_category.append(question['category'])
        current_category = list(set(current_category))
        return jsonify({
            "success": True,
            "questions":totalQuestions,
            "total_questions": lengthQuestions,
            "current_category": current_category,
            "categories": totalcategories
        })

    '''
      Create an endpoint to DELETE question using a question ID.
      TEST: When you click the trash icon next to a question, the question will be removed.
      This removal will persist in the database and when you refresh the page.
    '''
    @app.route("/questions/<questionId>", methods=['DELETE'])
    def question_deletion(questionId):
        try:
            questionDeletion = Question.query.filter(Question.id == questionId)
            questionDeletion.delete()
            db.session.commit()
            return jsonify({
                'success': True,
                'deleted': questionId
            })
        except:
            abort(422)




    '''
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route("/questions", methods=['POST'])
    def question_addition():
        recievedData = request.get_json()
        if not ('question' in recievedData and 'answer' in recievedData and 'difficulty' in recievedData and 'category' in recievedData):
            abort(422)
        recievedQuestion = recievedData.get('question')
        recievedAnswer = recievedData.get('answer')
        recieveddifficulty = recievedData.get('difficulty')
        recievedcategory = recievedData.get('category')
        if recievedQuestion and recievedAnswer and recieveddifficulty and recievedcategory:
            try:
                addNewQuestion = Question(
                    question=recievedQuestion,
                    answer=recievedAnswer,
                    difficulty=recieveddifficulty,
                    category=recievedcategory,
                )
                db.session.add(addNewQuestion)
                db.session.commit()
                pageNumbers = request.args.get('page', 1, type=int)
                # define the end the start point in paginition
                startingPoint = (pageNumbers - 1) * QUESTIONS_PER_PAGE
                endingPoint = startingPoint + QUESTIONS_PER_PAGE
                allQuestions = Question.query.filter().order_by(asc(Question.id))
                totalQuestions = [eachquestion.format() for eachquestion in allQuestions]
                totalQuestionsLength = len(totalQuestions)
                return jsonify({
                    'success': True,
                    'created': addNewQuestion.id,
                    'questions': totalQuestions[startingPoint:endingPoint],
                    'total_questions': totalQuestionsLength
                })

            except:
                abort(422)
        else:
            abort(422)



    '''
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/searching', methods=['POST'])
    def question_searchbox():
        searchbox_data = request.get_json()
        search_term = searchbox_data.get('searchTerm', None)
        search = "%{}%".format(search_term)
        # if write anything
        if search_term:
            search_results = Question.query.filter(Question.question.ilike(search)).all()
        #     if submit nothong it will 404 not found
        elif search_term == '':
            abort(404)

        # search_result_length = len(search_results)
        totalQuestions = [question.format() for question in search_results]
        # *****totalQuestions****
        if len(search_results):
            search_result_length = len(search_results)
        else:
            search_result_length = 0
        pageNumbers = request.args.get('page', 1, type=int)
        # define the end the start point in paginition
        startingPoint = (pageNumbers - 1) * QUESTIONS_PER_PAGE
        endingPoint = startingPoint + QUESTIONS_PER_PAGE
        totalQuestions = totalQuestions[startingPoint:endingPoint]
        # Get categories "current category"
        current_category = []
        for question in totalQuestions:
            current_category.append(question['category'])
        current_category = list(set(current_category))
        return jsonify({
                'success': True,
                'questions': totalQuestions,
                'total_questions': search_result_length,
                'current_category': current_category
        })


    '''
  Create a GET endpoint to get questions based on category.
  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category>/questions', methods=['GET'])
    def retrieving_Category_on_Click(category):
        try:
            category = str(category)
            allQuestion = Question.query.filter(Question.category == category).all()
            totalQuestions = [eachquestion.format() for eachquestion in allQuestion]
            if len(totalQuestions):
                total_questions =  len(totalQuestions)
            else:
                abort(404)
            return jsonify({
                'success': True,
                'questions':totalQuestions,
                'total_questions': total_questions,
                'current_category': category
            })
        except:
            abort(404)

    '''
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def quiz_retrival():
        quiData = request.get_json()
        quiz_category = quiData.get('quiz_category')
        previous_questions = quiData.get('previous_questions')
        # all
        if quiz_category['id'] == '0' or quiz_category['type'] == 'click' :
            allQuestions = Question.query.all()
        # other
        else:
            allQuestions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()
        totalQuestions = [eachquestion.format() for eachquestion in allQuestions]
        totalLength = len(totalQuestions)
        if totalLength:
            question =  random.choice(totalQuestions)
        else:
            question = None
            # abort(404)
        return jsonify({
                    'success': True,
                    'question': question
                })
    '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    return app