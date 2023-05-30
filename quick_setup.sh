cd estimation_quiz
echo "Settin up database tables"
python manage.py makemigrations
python manage.py migrate
echo "Resetting answers"
python manage.py reset_answers
echo "Importing questions"
python manage.py import_questions test_set.csv --delete-old-questions --silent
echo "Creating admin user"
python manage.py createsuperuser
