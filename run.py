# Code to run the file
from toodoo import create_app, db

app = create_app()

if __name__=='__main__':
    app.run(debug=True)