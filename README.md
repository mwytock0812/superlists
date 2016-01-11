#Superlists: A Django List Application
Superlists is a web application based off Harry Percival's book <a href="http://chimera.labs.oreilly.com/books/1234000000754">Test-Driven Development with Python</a>.

##Setting Up Development Environment
Superlists was developed using the following Python packages in an anaconda environment:

  * django 1.9
  * selenium 2.48.0

To set up the development environment:

  1. Install <a href="http://conda.pydata.org/docs/index.html">anaconda</a> for python 3.5.
  2. Create a new anaconda environment with django, and selenium
  ```
  conda create --name django-dev python=3.5 django selenium
  ```

  If anaconda yells that selenium cannot be found in the package repository, leave it off the install list, and install it using `pip` (covered next).
  3. Activate the new anaconda environment (and install selenium, if necessary).
  ```
  source activate django-dev
  ```

  If you still need to install selenium, run `pip install selenium` now that the environment is activated. To close the environment, use `source deactivate`.

##Clone the Superlists Repository
To clone this repo, run `git clone https://github.com/mwytock0812/superlists.git` from the desired destination directory.

##Running the Development Server
After navigating to the `superlists` directory, use the pre-packaged development server that comes with Django by running `python manage.py runserver`. Ensure that the correct conda environmenet is activated.

##Running Functional and Unit Tests
###Functional Tests
  1. Navigate to application's top level directory, `/superlists`
  2. Use Django's built-in testing suite to run functional tests
  ```
  python manage.py test functional_tests
  ```

**Note**: The `StaticLiveServerTestCase` class from which these test classes inherit includes a number of nice features including automatic setup and teardown by way of inheriting from `LiveServerTestCase` and truncation of the database tables by way of inheriting from `TransationTestCase`.

###Unit Tests
  1. Navigate to the applicaiton's top level directory, `/superlists`
  2. Use Django's built-in testing suite to run unit tests
  ```
  python manage.py test lists.tests
  ```

**Note**: The Django `TestCase` class used in these tests inherits from python's `unittest` module but adds the benefit of running each test as a transaction, providing isolation. Additionally, this only tests this lists app within Superlists. If more apps are added, each will be tested separately using dot notation or linked into the `manage.py test` runner.
