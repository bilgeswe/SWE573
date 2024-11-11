
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
