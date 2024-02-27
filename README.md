## How to start

- Clone the repository
```bash
git clone https://github.com/tegmark00/test-service.git
```
- Go to the project directory
```bash
cd test-service
```
- Create a virtual environment (python 12 or higher)
```bash
python3 -m venv venv
```
- Activate the virtual environment
```bash
source venv/bin/activate
```
- Install the requirements
```bash
pip install -r requirements.txt
```
- Create a .env file in the project directory
```bash
mv .env.example .env
```
- Run migrations
```bash
python manage.py migrate
```
- Collect static files
```bash
python manage.py collectstatic
```
- Run the server
```bash
python manage.py runserver
```

P.S. We use sqlite as a database for this project.
So you don't need to install any additional software.

## How to use

- Observe the API documentation at http://127.0.0.1:8000/api/swagger/
- Download api schema at http://127.0.0.1:8000/api/schema/
- Create a superuser and login to the admin panel at http://127.0.0.1:8000/admin/
- CRUD for clients: http://127.0.0.1:8000/api/service/clients/
- CRUD for requests: http://127.0.0.1:8000/api/service/requests/

## How to test
 - Install dev requirements with poetry from dev group
 - Run tests
```bash
pytest
```

## Main files:
- service/models.py - models for clients and requests
- service/api/* - CRUD for clients and requests
