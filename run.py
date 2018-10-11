from app import app
from flask import Flask, session



if __name__ == '__main__':

	app.secret_key = "super secret key"

	app.run()