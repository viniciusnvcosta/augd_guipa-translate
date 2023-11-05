from flask import Blueprint

test_bp = Blueprint('test',__name__)

class Test:
    @staticmethod
    @test_bp.route('/test',methods=['GET'])
    def get_test():
        return {'status': 'successo'}
  
   