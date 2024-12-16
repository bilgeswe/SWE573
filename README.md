
# Initialize the venv

python3 -m venv venv


# Activate venv

source venv/bin/activate


# Install requirements

pip3 install -r requirements.txt


# Migrate database

python3 forum/manage.py migrate

# Create admin user

python3 forum/manage.py createsuperuser

# Collect static files

python3 forum/manage.py collectstatic

# Run server

python3 forum/manage.py runserver

# Login trough admin panel

http://127.0.0.1:8000/admin/

## When Docker is the prefered way to deploy

# Docker compose up and build
docker-compose up -d --build

# Docker run migrations
docker-compose exec web python forum/manage.py migrate

# Docker compose down
docker-compose down

# Docker create superuser
docker-compose exec web python forum/manage.py createsuperuser

## When running tests, make sure you're in where manage.py is located
python manage.py test --settings forum.settings_dev
