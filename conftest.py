"""
Pytest is quite different from other popular unit testing, as it introduces the concept of fixtures. 
A fixture is just a named function, which constructs a test object (e.g. a mock database connection). 
Whenever a test function declares a formal parameter whose name coincides with the name of the fixture, pytest will invoke the corresponding fixture function and pass its result to the test.
"""

import pytest
from server.instance import server

# Creates a fixture whose name is "app"
# and returns our flask server instance
@pytest.fixture
def app():
    app = server.app
    return app