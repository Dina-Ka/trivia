# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment. "Dina"

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
in case you are working in windows 

```bash
SET FLASK_APP=flaskr
SET FLASK_ENV=development
flask run
```


Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
it used to retrieve the question in the main landing page 10 questions "per page" and total no of questions and the categories and categories
while request we send page no 
in case of not selecting a page "by default we are considing it one" 
returns the below :
[categories: {
​​
1: "Science"
​​
2: "Art"
​​
3: "Geography"
​​
4: "History"
​​
5: "Entertainment"
​​
6: "Sports"
},
current_category: [1,2,3,4,5],
questions: 
​​[
0: Object { answer: "Tom Cruise", category: 5, difficulty: 4, id: 4 }
​​
1: Object { answer: "Maya Angelou", category: 4, difficulty: 2, … }
​​
2: Object { answer: "George Washington Carver", category: 4, difficulty: 2, … }
​​
3: Object { answer: "Agra", category: 3, difficulty: 2, … }
​​
4: Object { answer: "Escher", category: 2, difficulty: 1, … }
​​
5: Object { answer: "Mona Lisa", category: 2, difficulty: 3, … }
​​
6: Object { answer: "One", category: 2, difficulty: 4, … }
​​
7: Object { answer: "Jackson Pollock", category: 2, difficulty: 2, … }
​​
8: Object { answer: "The Liver", category: 1, difficulty: 4, … }
​​
9: Object { answer: "Alexander Fleming", category: 1, difficulty: 3, … }],
total_questions: 30]

we use also delete method as I use it in the delete question end point in the redirection so /question should accepts both delete and get methods
​​```

DELETE /questions/questionId
it sends the queston id anf it retrn back the sucess true
after that it retrirve the main page to page = 1 as default

POST /questions
This end point used to create question
recieved data as
    {
            "answer":"answer test",
            "category": '5',
            "difficulty": '1',
            "question": 'question test test'
    }
and it returns
{
  created: 50,
  succuss: "true', 
 questions: 
​​[
0: Object { answer: "Tom Cruise", category: 5, difficulty: 4, id: 4 }
​​
1: Object { answer: "Maya Angelou", category: 4, difficulty: 2, … }
​​
2: Object { answer: "George Washington Carver", category: 4, difficulty: 2, … }
​​
3: Object { answer: "Agra", category: 3, difficulty: 2, … }
​​
4: Object { answer: "Escher", category: 2, difficulty: 1, … }
​​
5: Object { answer: "Mona Lisa", category: 2, difficulty: 3, … }
​​
6: Object { answer: "One", category: 2, difficulty: 4, … }
​​
7: Object { answer: "Jackson Pollock", category: 2, difficulty: 2, … }
​​
8: Object { answer: "The Liver", category: 1, difficulty: 4, … }
​​
9: Object { answer: "Alexander Fleming", category: 1, difficulty: 3, … }],
total_questions: 30]

}
```
POST /questions/searching
this post request send data in searchterm 
searchTerm : "Test" 
and it retrieve the data as per to the the data enter by user it calls back
{
    'success': True,
    'questions':[], //array of all question data as mentioned above
    'total_questions': 30, 
    'current_category': [] array of cat
}
```
GET /categories/<int:category>/questions
it recieves categoryId to filter by assigned for this category 
{
  'success': True,
  'questions':[], //array of all question data as mentioned above,
  'total_questions': 5,
  'current_category': 1
}

```
POST '/quizzes'
it sends 
{
"previous_questions": [],
"quiz_category": {
    "id": '1',
    "type": 'Art'
}
}
recieving 
{
'success': True,
'question': { answer: "Tom Cruise", category: 5, difficulty: 4, id: 4 }
}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```