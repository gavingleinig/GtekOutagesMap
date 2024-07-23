from os import environ
from GtekOutageMap import create_app

# Create the app instance
app = create_app()

# Define a main function to run the app directly (for development purposes)
def main():
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 8080)))

if __name__ == '__main__':
    main()