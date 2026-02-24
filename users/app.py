from webapp import create_app
"""
Entrypoint for the Users Microservice Flask application.

Creates and runs the Flask app using the factory function `create_app`.
"""

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')