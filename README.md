Install instructions
===========================

git clone git@github.com:Sashkow/FortyTwoTestTask2.git
cd FortyTwoTestTask2
virtualenv --no-site-packages .env
source .env/bin/activate
.env/bin/pip install -r requirements.txt
python manage.py syncdb --noinput
python manage.py migrate
python manage.py syncdb --noinput


42-test template
===========================

A Django 1.6+ project template

Use fortytwo_test_task.settings when deploying with getbarista.com

### Recomendations
* apps in apps/ folder
* use per-app templates folders
* use per-app static folders
* use migrations
* use settings.local for different environments
* common templates live in templates/
* common static lives in assets/
* management commands should be proxied to single word make commands, e.g make test

