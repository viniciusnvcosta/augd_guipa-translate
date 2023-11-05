from flask import Flask
import controller

def create_app():
    app = Flask(__name__)
    
    controller.init_bp(app)
    
    return app


if __name__=='__main__':
    app = create_app()
    app.run(debug=True)