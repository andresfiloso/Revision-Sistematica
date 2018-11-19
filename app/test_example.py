import os
import sqlite3
import pytest
import sys

from app import *


@pytest.fixture(scope='function')
def login(username, password):
    return self.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def test_login_logout():
    """Make sure login and logout works."""

    rv = login("admin", "admin")
    assert b'You were logged in' in rv.data

    



