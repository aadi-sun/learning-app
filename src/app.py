from socket import gethostname
#creating flask app

from website import create_app
app = create_app()
if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(debug=True)



    
    




