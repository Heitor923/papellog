web: cd backend && gunicorn papellog.wsgi
release: cd backend && python manage.py collectstatic --noinput && python manage.py migrate
