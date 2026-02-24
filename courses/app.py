"""
Entry point for the Flask application.

Creates the app using `create_app` and runs it on host 0.0.0.0
with debug mode enabled.
"""

from webapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')