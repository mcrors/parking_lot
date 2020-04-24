# Instalation in development Environment

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
    
The application has also been tested with curl and Postman.


# Usage

## add

Used to add a car to the parking lot.

**URL** : `/add`

**Method** : `GET`

**Auth required** : NO

**Data constraints**

Must contain query parameters:
* car (the registration number of the car)
* tariff (the tariff name)

**Usage example**

/add?car=X774HY98&tariff=hourly

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success", 
  "car": "X774HY98", 
  "tariff": "hourly", 
  "location": 12, 
  "start": "2014-10-01 14:11:45"
}
```

## Error Response

**Condition** : If 'car' or 'tariff' are not supplied.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "You must supply both a car registration number and tariff"
}
```


**Condition** : If the car registration number supplied is already located in the parking lot.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "A car with the registration number {value} is already parked here"
}
```


**Condition** : If the tariff value supplied does not match a valid tariff plan

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "The tariff type {value} is not available or does not exist"
}
```


**Condition** : If there are no available spaces left in the parking lot

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "No free spaces"
}
```


## remove

Used to remove a car to the parking lot.

**URL** : `/remove`

**Method** : `GET`

**Data constraints**

Must contain query parameters:
* location (the location that the car being removed was assigned)

**Usage example**

/remove?location=1

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success", 
  "car": "X774HY98", 
  "tariff": "hourly", 
  "location": 12, 
  "start": "2014-10-01 14:11:45",
  "finish": "2014-10-01 14:21:45",
  "fee": 0
}
```

## Error Response

**Condition** : If location is not supplied.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "You must supply a location number"
}
```


**Condition** : If location value provided is not a number

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "Location value entered {value} is not an integer. You must supply an integer value"
}
```


**Condition** : The location value provided is does not exist in the parking lot

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "The location {value} does not exist"
}
```


**Condition** : The location provided was not occupied.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
  "status": "error",
  "message": "Location {value} was not occupied"
}
```


## list

Used to list all cars that a currently parked in the parking lot.

**URL** : `/list`

**Method** : `GET`

**Data constraints**

None

**Usage example**

/list

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "status": "success", 
  "cars": [
      {"car": "X774HY98", "tariff": "hourly", "location": 1, "start": "2014-10-01 14:11:45"},
      {"car": "X637TT98", "tariff": "daily", "location": 2, "start": "2014-10-01 15:23:05"}
  ]
}
```