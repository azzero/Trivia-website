Getting Started:
Pre-requisites and Local Development:

Developers using this project should already have Python3, pip and node installed on their local machines.

Backend
From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

These commands put the application in development and directs our application to use the **init**.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

---

## Frontend

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

From the frontend folder, run the following commands to start the client:
npm install // only once to install dependencies
npm start
By default, the frontend will run on localhost:3000.

---

## Tests

In order to run tests navigate to the backend folder and run the following commands:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

---

## API :

GET /categories :

- General:
  Returns an object that contains categories object, success value, and total number of categories
- Sample: curl http://127.0.0.1:5000/categories
  {
  "categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  },
  "success": true,
  "total_categories": 6
  }

GET /questions :
General:
Returns an object that contains list of questions , success value,categories,current category and total number of questions
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/questions
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
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
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
}
],
"success": true,
"total_questions": 24
}

POST /questions :
General:
Creates a new question using the submitted question, answer , difficulty and category. Returns success value,
curl -X POST -d '{"question":"what is the capital of morocco " , "answer":" rabat ","difficulty":2,"category":2}' -H "Content-Type:application/json" http://127.0.0.1:5000/questions;

{
"success": true
}

DELETE /questions/{question_id}
General:
Deletes the question of the given ID if it exists. Returns success value
curl -X DELETE http://127.0.0.1:5000/questions/32
{
"success": true
}

POST /question/search:
General:
searching for some questions based on search term , Returns an object of questions,success value, total number of questions , categories and current category

- Sample : curl -X POST -d '{"searchTerm":"title"}' -H "Content-Type:application/json" http://127.0.0.1:5000/questions/search

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
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
{
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
}
],
"success": true,
"total_questions": 26
}

GET /categories/{categorie_id}/questions:
General :
get questions by category , Returns an object that contains questions , success value, total number of questions and current category

- Sample : curl http://127.0.0.1:5000/categories/1/questions

{
"current_category": "1",
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
},
{
"answer": "azzeddine",
"category": 1,
"difficulty": 1,
"id": 31,
"question": "what is my name "
}
],
"success": true,
"total_questions": 4
}

POST /quizzes :
General :
get questions to play the quiz,Returns and object that contains the next question and success value .
Sample : curl -X POST -d '{"previous_questions":[5] , "quiz_category":{"id":1}}' -H "Content-Type:application/json" http://127.0.0.1:5000/quizzes
{
"question": {
"answer": "Alexander Fleming",
"category": 1,
"difficulty": 3,
"id": 21,
"question": "Who discovered penicillin?"
},
"success": true
}
