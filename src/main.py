"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Person
import datetime 
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    people=Person.query.all()
    all_people=list(map(lambda person:person.serialize(),people))

    if all_people==[]:
        return jsonify('Nothing here!')
    else:
        return jsonify(all_people), 200

@app.route('/newperson',methods=['POST'])
def create_person():
    request_body=request.get_json()
    name=request.json.get('name',None)
    last_name=request.json.get('last_name',None)
    age=request.json.get('age',None)
    if not name:
        return jsonify({'msg':'Name required'}),400
    if not last_name:
        return jsonify({'msg':'Last Name required'}),400
    if not age:
        return jsonify({'msg':'Age of birth required'}),400
    
    newPerson = Person(name=name, last_name=last_name,age=age)
    db.session.add(newPerson)
    db.session.commit()
    return jsonify(request_body),200

@app.route('/person/<int:person_id>')
def get_person(person_id):
    person=Person.query.get(id)

    ############### Children ###############
    child_id =Person.query.filter_by(mother_id=person_id)
    print('child1',child_id)
    if not child_id:
        child_id2 =Person.query.filter_by(father_id=person_id)
        print('child',child_id2)

    ############ Parents ######################
    mother_id=person.mother_id
    father_id=person.father_id
    mother=Person.query.filter_by(mother_id=mother_id)
    father=Person.query.filter_by(father_id=father_id)

    print('parents',mother,father)
    ############### Grand Parents ##############
                        ########### Mother Parents
    grand_ma_id_mother= mother.mother_id
    grand_pa_id_mother= mother.father_id
    grand_ma_mother=Person.query.filter(mother_id=grand_ma_id_mother)
    garnd_pa_mother =Person.query.filter(father_id=grand_pa_id_mother)

    print('gandMother',grand_ma_mother,garnd_pa_mother)
                        ########### Father Parents
    grand_ma_id_father= father.mother_id
    grand_pa_id_father= father.father_id
    grand_ma_father=Person.query.filter(mother_id=grand_ma_id_father)
    garnd_pa_father =Person.query.filter(father_id=grand_pa_id_father)
    print('gandFather',grand_ma_father,garnd_pa_father)
    


    return jsonify(person.serialize())

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
