import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    

    '''
  @todo: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    #Todo: Use the after_request decorator to set Access-Control-Allow
    
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                        'GET,PUT,POST,DELETE,OPTIONS')
      return response

  #todo: Create an endpoint to handle GET requests 

    @app.route("/categories")
    def all_categories():
      categories = Category.query.all()
      return jsonify({
        'success': True,
        "categories": {categorie.id:categorie.type for categorie in categories},
        "total_categories": len(categories)

    })
  #TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
    @app.route("/questions")
    def all_question():
      selections=Question.query.order_by(Question.id).all()
      current_questions=paginate_questions(request,selections)
      categories=Category.query.order_by(Category.id).all()
      if len(current_questions)==0:
        abort(404)
      return jsonify({
        'success':True,
        "questions":current_questions,
        "total_questions":len(Question.query.all()),
        "categories": {categorie.id:categorie.type for categorie in categories},
        "current_category":None
      })
  #TEST: At this point, when you start the application you should see questions and categories generated, ten questions per page and pagination at the bottom of the screen for three pages. Clicking on the page numbers should update the questions. 
  #todo: Create an endpoint to DELETE question using a question ID. 
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
      try:
        question=Question.query.filter(Question.id==question_id).one_or_none()
        if (question is None ):
          abort(404)
        else:
          question.delete()
      except:
        abort(422)
  #TEST: When you click the trash icon next to a question, the question will be removed This removal will persist in the database and when you refresh the page. 
  #done
  #todo: Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
  #TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last pageof the questions list in the "List" tab.  
   #done 
    @app.route("/questions", methods=["POST"])
    def add_question():
      try:
          body=request.get_json()
          question_value=body.get("question",None)
          answer_value=body.get("answer",None)
          difficulty_value=body.get("difficulty",None)
          category_value=body.get("category",None)
          question=Question(question=question_value,answer=answer_value,difficulty=difficulty_value,category=category_value)
          question.insert()
          return jsonify({
            "success":True
          })
      except:
        abort(422)

  #todo Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
    @app.route("/questions/search" ,methods=["POST"])
    def search_for_question():
      try:
          term=request.get_json()["searchTerm"]
          searchTerm="%{}%".format(term)
          selections=Question.query.filter(Question.question.ilike(searchTerm))
          current_questions=paginate_questions(request,selections)
          categories=Category.query.order_by(Category.id).all()
          if len(current_questions)==0:
            abort(404)
          return jsonify({
            'success':True,
            "questions":current_questions,
            "total_questions":len(Question.query.all()),
            "categories": {categorie.id:categorie.type for categorie in categories},
            "current_category":None
          })
      except:
        abort(422)
  #TEST: Search by any phrase. The questions list will update to include only question that include that string within their question. Try using the word "title" to start. 
  #done
  #todo: Create a GET endpoint to get questions based on category. 
    @app.route("/categories/<category_id>/questions")
    def get_questions_by_category(category_id):
      try:
        selections=Question.query.filter(Question.category==category_id).all()
        current_questions=paginate_questions(request,selections)
        if len(current_questions)==0:
          abort(404)
        return jsonify({
          "questions":current_questions,
          "total_questions":len(selections),
          "current_category":category_id
        })
      except:
        abort(422)
  #TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. 
   #done
  #todo:Create a POST endpoint to get questions to play the quiz. his endpoint should take category and previous question parameters  and return a random questions within the given category, if provided, and that is not one of the previous questions. 
    @app.route("/quizzes" , methods=["POST"])
    def quizze():
      try:
        body=request.get_json()
        previous_questions=body.get("previous_questions",None)
        quiz_category=body.get("quiz_category",None)
        # print(previous_questions)
        # print(quiz_category)
        # question=Question.query.get(2)
        questions_lottery=[]
        if quiz_category['id']==0:
          questions=Question.query.all()
        else:
          questions=Question.query.filter(Question.category==quiz_category["id"]).all()
        questions_formated=[question.format() for question in questions]
        print(questions)
        for q in questions_formated:
          if q['id'] not in previous_questions:
            
            questions_lottery.append(q)
        if len(questions_lottery) > 0:
          question=random.choice(questions_lottery)
        else:
          question=None
        return jsonify({
        "question":question,    
    })
      except:
        abort(422)
  #TEST: In the "Play" tab, after a user selects "All" or a category,one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not. 
    #done
  #todo: Create error handlers for all expected errors  including 404 and 422. 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request "
        }), 400
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }),422
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }),405
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }),500
    return app








    




  


  



  



  






  


