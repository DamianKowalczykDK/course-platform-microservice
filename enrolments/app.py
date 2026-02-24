from webapp import create_app

"""
Entrypoint for the Enrolments microservice.

Creates the Flask app using the factory pattern and starts the development server.
"""

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')