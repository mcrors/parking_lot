To install development environment, perform the following steps

1. Ensure that you have python 3.7 installed on your machine.
2. Ensure that you have pip installed on your machine.
3. Install pipenv:
    pip install pipenv
4. Clone the repository to your local development machine.
5. Install dependencies using pipenv:
    pipenv install .
6. Activate the virtual environment:
    pipenv shell
7. Install the application in editiable mode:
    pip install -e .
8. Set flask environment variables:
    Linux/Mac:
        $ export FLASK_APP=parking_lot
        $ export FLASK_ENV=development
    Windows:
        > set FLASK_APP=parking_lot
        > set FLASK_ENV=development
9. Run tests:
    pytest --cov=app ./tests -v
10. Run the application:
    flask run
    
The application has been tested with curl and Postman.