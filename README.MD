The required dependancies is located in the `requirements.txt` file

To install:
open terminal (not venv terminal) and type `pip install -r requirements.txt`

Remember to update the requirements.txt file if you install any new dependancies via `pip install <dependancy>` and `pip freeze > requirements.txt`

requires `CLERK_API_KEY` to be set in the environment variables, which is the bearer token from your Clerk account

if using Pycharm: in your python interpreter settings, add the environment variable `CLERK_API_KEY` with the value of your clerk api key