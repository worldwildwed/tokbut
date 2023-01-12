pip install django
pip install psycopg2-binary
django-admin startproject $APPNAME_django .
django-admin startapp $APPNAME

>>> postgresql-cli
psql -d postgres
CREATE DATABASE $APPNAME;
CREATE USER $user WITH PASSWORD 'password';
<>
> GRANT ALL PRIVILEGES ON DATABASE $APPNAME TO $user;
> GRANT ALL PRIVILEGES ON SCHEMA public to $user;
> GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tunruser;
