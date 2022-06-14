# API Reference

## Getting Started
- Base URL: Currently this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.


## Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False, 
    "error": 422,
    "message": "unprocessable"
}
```

The API will return three error types when requests fail:

- 422: Unprocessable
- 400: Bad Request
- 404: Resource Not Found 

## Endpoints

## GET/categories

- General:
  - Returns a list of categorie objects and success value.
- Sample: GET http://127.0.0.1:5000/categories

```json
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"success": true
}
```

## GET/questions

- General:
   - Returns a list of questions objects, success value, total questions, total questions and current category.
   - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: GET http://127.0.0.1:5000/questions

```json
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": null,
	"questions": [
		{
			"answer": "Brazil",
			"category": 6,
			"difficulty": 3,
			"id": 10,
			"question": "Which is the only team to play in every soccer World Cup tournament?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 3,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		},
		{
			"answer": "Agra",
			"category": 3,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
		},
		{
			"answer": "Escher",
			"category": 2,
			"difficulty": 1,
			"id": 16,
			"question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
		},
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "One",
			"category": 2,
			"difficulty": 4,
			"id": 18,
			"question": "How many paintings did Van Gogh sell in his lifetime?"
		},
		{
			"answer": "Jackson Pollock",
			"category": 2,
			"difficulty": 2,
			"id": 19,
			"question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		}
	],
	"success": true,
	"totalQuestions": 30
}
```

## DELETE/questions/id

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- Sample: DELETE http://127.0.0.1:5000/questions/id

```json
{
	"deleted": 19,
	"success": true
}
```

## POST/questions

- General:
  - Creates a new question using the submitted question, answer, difficulty and category. Returns the id of the created question, success value and
      a message.
- Sample: POST http://127.0.0.1:5000/questions 

```json
{
	"created": 43,
	"massage": "question created",
	"success": true
}
``` 

### POST/questions/search_question

- General:
  - It search for questions using a SearchTerm. Returns all questions with the SearchTerm, success value, total question and current category.
  -  Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: POST http://127.0.0.1:5000/questions/search_question 

```json
{
	"current_category": null,
	"questions": [
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		}
	],
	"success": true,
	"totalQuestion": 4
}
``` 

### GET/categories/id/questions

- General:
  - It fetch questions of  a given category ID if exist. Returns all questions of the category, success value, total question and current category.
  -  Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: GET http://127.0.0.1:5000/categories/id/questions

```json
{
	"current_category": "Science",
	"questions": [
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		}
	],
	"success": true,
	"totalQuestion": 3
}
```

### POST/quizzes

- General:
  - Creates a new quiz using the category ID and privious quiz questions. Returns question and success value.
- Sample: POST http://127.0.0.1:5000/quizzes

```json
{
	"question": {
		"answer": "Blood",
		"category": 1,
		"difficulty": 4,
		"id": 22,
		"question": "Hematology is a branch of medicine involving the study of what?"
	},
	"success": true
}
```






