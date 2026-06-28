@echo off
cd /d %~dp0
echo ============================================
echo First Time Setup - Finance Complaince Web Application
echo ============================================
py -3.12 -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_services
echo.
echo Setup completed. Create admin user using:
echo python manage.py createsuperuser
pause
