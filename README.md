# Estimathon
A Django webapp implementing an estimation based quiz.


## Importing questions
Questions can be imported with the management tool, `import_questions`. Place the file *my_questions_file.csv* in estimation_quiz/quiz/questions/ formatted as follows:
```csv
How many continents are there?; 7
What is the answer to life, the universe, and everything?; 42
...
```

Now, to import my_questions_file.csv navigate to the topmost estimation_quiz folder and run the following command:
```
    python manage.py import_questions my_questions_file
```
There are three optional flags to the function:
- `--delete-old-questions`: Removes all previous questions from the database.
- `--deactivate-old-questions`: Retains previous questions but makes them inactive, i.e., they will not be part of the quiz.
- `--silent`: Suppresses output

An example is
```
    python manage.py import_questions my_questions_file --delete-old-questions
```
