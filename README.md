# Dog
[![Build Status](https://travis-ci.org/inno-asiimwe/flask_assessment.svg?branch=develop)](https://travis-ci.org/inno-asiimwe/flask_assessment)
[![Coverage Status](https://coveralls.io/repos/github/inno-asiimwe/flask_assessment/badge.svg?branch=develop)](https://coveralls.io/github/inno-asiimwe/flask_assessment?branch=develop)

## Introduction
A simple API built in Flask used for an assessment exercise and LMS output submission

### Endpoints implemented 
- `GET` /api/v1/breeds
- `POST`/api/v1/breeds
- `GET` /api/v1/breeds/<breed_id>
- `PUT` /api/v1/breeds/<breed_id>
- `DELETE` /api/v1/breeds/<breed_id>
- `GET` /api/v1/dogs
- `GET` /api/v1/dogs/<dog_id>
- `POST` /api/v1/dogs
- `GET` /api/v1/statistics
- `GET` /api/v1/statistics?breed=<breed_id>

### Request structure examples
#### Breed Resource Request
```
{
    "name": "bulldog",
    "description": "Guard dog"
}
```
#### Dog Resource Request
```
{
    "name": "fox",
    "breed": 1,
    "age": 12,
    "weight": 25.6,
    "color": "black"
}
```