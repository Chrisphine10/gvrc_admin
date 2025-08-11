# Built with [Django App Generator](https://app-generator.dev/tools/django-generator/)

Starter generated with [Django Generator](https://app-generator.dev/tools/django-generator/) (an open-source service) using **Gradient Design**, best practices and up-to-date Dependencies.
In order to use the sources, follow the build instructions as presented in `Start with Docker` and `Manual Build` sections. 

- Get [Support](https://app-generator.dev/ticket/create/?generated_repo=https://github.com/app-generator/django-gradient-1754404928) via `eMail` and `Discord`
- Resources:
  - [Getting Started with Django](https://app-generator.dev/docs/technologies/django/index.html)
  - [Onboarding Kit for Developers](https://app-generator.dev/onboarding-kit/) - Premium resources for coding services in no-time.
  - [Discounts for Developers](https://app-generator.dev/discounts) - Build your own dev bundle and start fast 
  - [Build Dynamic Services with Django](https://app-generator.dev/docs/developer-tools/dynamic-django/index.html)
  
<br />

## Features: 

- `Up-to-date Dependencies`, Best practices
- Desing: Gradient
- Extended User Profile 
- (optional) API Generator
- (optional) Celery
- (optional) OAuth Github, Google
- (optional) CI/CD for Render
- (optional) Docker

<br />

## [Deploy on Render](https://app-generator.dev/docs/deployment/render/index.html) (free plan)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

<br /> 

## [Start Project with Docker](https://app-generator.dev/docs/technologies/docker/index.html)

> In case the starter was built with Docker support, here is the start up CMD:

```bash
$ docker-compose up --build
```

Once the above command is finished, the new app is started on `http://localhost:5085`

<br />

## Manual Build 

> Download/Clone the sources  

```bash
$ git clone https://github.com/django-gradient-1754404928.git
$ cd django-gradient-1754404928
```

<br />

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> `Set Up Database`

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> `Start the App`

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />





---
Starter built with [Django App Generator](https://app-generator.dev/tools/django-generator/) - Open-source service for developers and companies.


## Things to remove

<!-- Remove test API endpoints - Delete the test views and URLs -->

Restore authentication - Remove @permission_classes([AllowAny]) decorators

Remove email signals - Delete the automatic email functionality

Clean up files - Remove test files like user_management.py and signals.py

Revert settings - Restore original email and authentication settings

## Running tests

pytest
pytest -v                    # verbose output
pytest tests/test_api.py     # specific test file

## Running pytest

# Install dependencies first
pip3 install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with database reuse (faster)
pytest --reuse-db


### API TEST RUNNER

http://localhost:8000/api/test-runner/

AFTER DEPLOYMENT IT WILL BE VISIBLE FOR EVERYONE

1. Prevent Breaking Changes
Ensure API still works after code updates

Catch bugs before they reach production

Verify endpoints return correct data formats

2. Validate Business Logic
Test authentication/authorization works

Verify data validation rules

Ensure proper error handling

3. Integration Confidence
Frontend developers know APIs work reliably

Mobile apps can depend on consistent responses

Third-party integrations won't break

4. Documentation Through Code
Tests show how APIs should be used

Examples of expected request/response formats

Living documentation that stays current

5. Regression Prevention
Automatically catch when old features break

Run tests before every deployment

CI/CD pipeline validation

6. Performance Monitoring
Track API response times

Identify slow endpoints

Ensure scalability requirements


