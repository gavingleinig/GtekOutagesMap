from os import environ
from GtekOutageMap import create_app

# Create the app instance
app = create_app()

# Define a main function to run the app directly (for development purposes)
def main():
    app.run(environ.get('FLASK_HOST'), port=environ.get('FLASK_PORT'))

if __name__ == '__main__':
    main()