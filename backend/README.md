# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting Endpoints

### Documentation of Some Endpoints

`GET '/categories'`

- Returns: All categories
- URI:- http://127.0.0.1:5000/categories
- Response

```json
{
  "categories": {
    "1": "history",
    "2": "science",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET '/questions'`

- Fetches:

  - A dictionary of all categories
  - The current category
  - A list of questions - 10 questions per page
  - The number total of questions

- Request arguments:

  - `page` (integer) - The current page

- Returns: An object with these keys:
  - `categories`: A dictionary of categories
  - `questions`: A list of questions - 10 questions per page
  - `current_category`: The current category
  - `success`: The success flag
  - `total_questions`: The total of questions

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
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
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
    }
  ],
  "success": true,
  "total_questions": 34
}
```

`DELETE /questions/<int:id>'`

- Returns: Deleted question with given ID.
- URI:- http://127.0.0.1:5000/questions/12
- Response

```json
{
  "id": 12,
  "message": "Question deleted successfully ",
  "success": true
}
```

`POST /'questions'`

- Inserting a new question
- Request arguments:
  - `answer` (string) - The answer
  - `category` (string) - The question category
  - `difficulty` (string) - The question difficulty
  - `question` (string) - The question
- URI:- http://127.0.0.1:5000/questions
- JSON file format

```json
{
  "answer": "blue",
  "category": "2",
  "difficulty": 1,
  "id": 10,
  "question": "What is the colour of sky"
}
```

- Response

```json
{
  "question": {
    "answer": "blue",
    "category": "2",
    "difficulty": 1,
    "id": 17,
    "question": "What is the colour of sky"
  },
  "success": true
}
```

`POST /'questions/search'`

- Search a question.
- Request arguments:
  - `searchTerm` (string) - The term to search
- Returns: An object with these keys:
  - `searchTerm`: The search term object containing the question searched for, its answer, category and difficulty
  - `current_category`: The current category
  - `success`: The success flag
  - `total_questions`: The total number of questions with the search term
- JSON file format

```json
{
  "searchTerm": "title"
}
```

- Response

```json
{
  "SearchTerm": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "current_category": null,
  "success": true,
  "total_questions": 1
}
```

`GET 'categories/<int:category_id>/questions'`

- Fetches a list of questions based on category.
- Request arguments:
  - `category_id` (integer): The category id
- Returns: An object with these keys:
  - `current_category`: The current category
  - `questions`: A list of questions in that category
  - `success`: The success flag
  - `total_questions`: The total of number questions in that category
  
- Response for URI http://127.0.0.1:5000/categories/2/questions

```json
{
  "current_categories": 2,
  "questions": [
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
    }
  ],
  "succeed": true,
  "total_questions": 4
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Errors

### Error 400

- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```

### Error 404

- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

### Error 405

- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

### Error 422

- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 422,
  "message": "unprocessable"
}
```
