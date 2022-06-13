import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "11223344E", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # trial question for testing create_question()
        self.question = {
            "question": "what is the slogan of cross river state, Nigeria?",
            "answer": "The nations paradise",
            "difficulty": 5,
            "category": 2,
        }

        # test request for testing play_quiz()
        self.quize = {
            "quiz_category": {"type": "Geography", "id": 2},
            "previous_questions": [16, 7],
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_question(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        # check equality of response value using assertEqual
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # compare  response value using assertTrue
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))

    def test_404_request_beyound_valid_page(self):
        res = self.client().get("questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_question_request(self):
        res = self.client().post(
            "/questions/search_question", json={"searchTerm": "What is"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestion"])
        self.assertTrue(len(data["questions"]))

    def test_if_search_question_request_failed(self):
        res = self.client().post(
            "/questions/search_question", json={"searchTerm": "buhari"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question_request(self):
        res = self.client().delete("/questions/27")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 27).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 27)

    def test_422_question_request_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_question_request(self):
        res = self.client().post("/questions", json=self.question)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data["success"], True)
        self.assertTrue(data["created"])

    def test_400_create_question_request_failed(self):
        res = self.client().post("/questions")
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 400)
        self.assertEquals(data["success"], False)
        self.assertEqual(data["message"], "bad_request")

    def test_obtain_questions_by_category_request(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestion"])
        self.assertTrue(data["current_category"])

    def test_404_obtain_questions_by_category_request_fails(self):
        res = self.client().get("/categories/9/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_request_for_play_quiz(self):
        res = self.client().post("/quizzes", json=self.quize)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data["success"], True)
        self.assertTrue(data["question"])

    def test_422_request_for_play_quiz_failed(self):
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 422)
        self.assertEquals(data["success"], False)
        self.assertTrue(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
