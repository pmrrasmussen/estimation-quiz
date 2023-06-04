# Estimathon
A Django webapp implementing an estimation based quiz. Further features and instructions on setting up a quiz are coming soon!

## Installation
Steps:
- Install requirements from requirements.txt. Note that I have experienced problems running the web app in the base conda environment, so either create a new environment or run the app through something other than conda.
- From the root of the repository, run `source quick_setup.sh`. It will setup:
    * Database for the app
    * Import test batch of answers
    * An admin account for the app
- From the estimation_quiz folder, execute `python manage.py runserver` to start the web app.
- Go to [https://localhost:8000/quiz](http://localhost:8000/quiz) to access the web app
- To add contestants (users) to the quiz, manage questions, and more, go to [https://localhost:8000/admin](http://localhost:8000/admin) to access admin features

## Managing the web app
Like any other Django-webapp, management of the application happens with the Django management tool. To access it, navigate the the topmost *estimation_quiz* folder and run
```
    python manage.py my_command
```

## Importing questions
Questions can be imported with the management tool, `import_questions`. Place the file *my_questions_file.csv* in *estimation_quiz/quiz/questions/* formatted as follows:
```csv
    How many continents are there?; 7
    What is the answer to life, the universe, and everything?; 42
    ...
```

Now, to import *my_questions_file.csv* run the following command:
```
    python manage.py import_questions my_questions_file.csv
```
There are three optional flags to the function:
- `--delete-old-questions`: Removes all previous questions from the database.
- `--deactivate-old-questions`: Retains previous questions but makes them inactive, i.e., they will not be part of the quiz.
- `--silent`: Suppresses output

An example:
```
    python manage.py import_questions my_questions_file.csv --delete-old-questions
```

## Resetting results
If the answers have been edited or results removed, it is possible to reset the results table as though the answers currently in the database were the only ones every given. It is done with the command
```
    python manage.py reset_results
```
