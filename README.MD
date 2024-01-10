The required dependancies is located in the `requirements.txt` file

To install:
open terminal (not venv terminal) and type `pip install -r requirements.txt`

Remember to update the requirements.txt file if you install any new dependancies via `pip install <dependancy>` and `pip freeze > requirements.txt`

requires `CLERK_API_KEY`, `SVIX_<OPTION>_KEY`, `MONGODB_URI` and `STRIPE_API_KEY`  to be set in the environment variables.

To run this script: `python app.py -m flask run`

Supports running as a flask app or as a script, but requires the environment variable `FLASK_ENV` to be set as `production` for gunicorn or any WSGI server to host, or `development` to run as a script.