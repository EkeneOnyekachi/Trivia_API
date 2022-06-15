from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers

    @app.after_request
    def after_request(response):

        try:
            response.headers.add(
                "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
            )
            response.headers.add(
                "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
            )
            return response
        except Exception as erro:
            print(erro)

    @app.route("/categories")
    def obtain_categories():

        try:
            # create dictionary object
            categorization = {}

            categories = Category.query.order_by(Category.id).all()
            for category in categories:
                # add item to dictionary cat
                categorization[category.id] = category.type

            if len(categories) == 0:
                abort(404)

            return jsonify({"success": True, "categories": categorization})
        except Exception as error:
            print(error)

    @app.route("/questions")
    def obtain_questions():

        categorization = {}

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        Categories = Category.query.order_by(Category.id).all()
        for category in Categories:
            categorization[category.id] = category.type

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection),
                "categories": categorization,
                # used None to indicate No value at all for(current_category)
                "current_category": None,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):

        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({"success": True, "deleted": question.id})
        except Exception as error:
            print(error)
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():

        try:
            body = request.get_json()

            new_question = body.get("question")
            new_answer = body.get("answer")
            new_difficulty = body.get("difficulty")
            new_category = body.get("category")

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category,
                )

                question.insert()

                return jsonify(
                    {
                        "success": True,
                        "massage": "question created",
                        "created": question.id,
                    }
                )
            except Exception as erro:
                print(erro)
                abort(422)
        except Exception as erro:
            print(erro)
            abort(400)

    @app.route("/questions/search_question", methods=["POST"])
    def search_question():

        body = request.get_json()

        # Get search item
        search_item = body.get("searchTerm", " ")
        # used ilike to make the match case insensitive
        selection = Question.query.filter(
            Question.question.ilike("%" + search_item + "%")
        ).all()

        current_question = paginate_questions(request, selection)
        if len(current_question) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_question,
                "totalQuestion": len(current_question),
                "current_category": None,
            }
        )

    @app.route("/categories/<int:category_id>/questions")
    def obtain_questions_by_category(category_id):

        try:
            # Get category id
            categorization = Category.query.filter(
                Category.id == category_id
            ).one_or_none()

            selection = Question.query.filter(
                Question.category == categorization.id
            ).all()

            category_questions = paginate_questions(request, selection)
            if len(category_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": category_questions,
                    "totalQuestion": len(category_questions),
                    "current_category": categorization.type,
                }
            )
        except Exception as erro:
            print(erro)
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():

        body = request.get_json()

        # Get category and previous quiz questions
        category = body.get("quiz_category")
        previous_quiz_questions = body.get("previous_questions")

        if category is None or previous_quiz_questions is None:
            abort(422)

        """Get question  category. used notin_ operator to get only 
            questions that does not belong to (previous_questions)"""
        if category["id"] == 0:
            possible_questions = Question.query.all()
        else:
            possible_questions = (
                Question.query.filter_by(category=category["id"])
                .filter(Question.id.notin_((previous_quiz_questions)))
                .all()
            )

        question = possible_questions[random.randrange(0, len(possible_questions), 1)]

        if len(possible_questions) > 0:
            return jsonify({"success": True, "question": question.format()})
        else:
            return None

    # Error handling

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad_request"}), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app
