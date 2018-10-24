import pytest
from flask import Flask

import sys
sys.path.insert(0,'..')
from app import app


def login(user, password):
    return post('/login', data=dict(
        user = user,
        password = password
    ), follow_redirects=True)



def test_login_logout():
    """Make sure login and logout works."""

    rv = login("admin", "admin")
    assert b'You were logged in' in rv.data

    rv = login("opkluijkyu", "admin")
    assert b'Invalid username' in rv.data

    rv = login("admin", "opkluijkyu")
    assert b'Invalid password' in rv.data