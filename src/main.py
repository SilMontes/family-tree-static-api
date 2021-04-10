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
from models import db, Person, PeopleRelationship
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
#------GET ALL PEOLPLE--------------------------------------------
@app.route('/people', methods=['GET'])
def get_all_people():
    people=Person.query.all()
    all_people=list(map(lambda person:person.serialize(),people))

    if all_people==[]:
        return jsonify('Nothing here!'),200
    else:
        return jsonify(all_people), 200
#------------------GET ALL RELATIONSHIPS-----------------
@app.route('/relationships', methods=['GET'])
def get_relationship():
    relationships=PeopleRelationship.query.all()
    all_relationships=list(map(lambda item:item.serialize(),relationships))

    if all_relationships == []:
        return jsonify('Nothing here!'),200
    else:
        return jsonify(all_relationships),200

#----------ADD A PERSON----------------------------------------
@app.route('/newperson',methods=['POST'])
def create_person():
    request_body=request.get_json()
    if request_body == {} or request_body == [] or request_body==None:
        return jsonify('Empty Request'),400
    name=request.json.get('name',None)
    last_name=request.json.get('last_name',None)
    age=request.json.get('age',None)

    if not name:
        return jsonify({'msg':'Name Required'}),400
    elif not last_name:
        return jsonify({'msg':'Last Name Required'}),400
    elif not age:
        return jsonify({'msg':'Age Required'}),400
    else:
        newPerson=Person(name=name,last_name=last_name,age=age)
        db.session.add(newPerson)
        db.session.commit()
    
    return jsonify(request_body),200

#--------------CREATE RELATIONSHIP---------------------------------------------
@app.route('/create_relationship', methods=['POST'])
def create_relationship():
    request_body=request.get_json()
    if request_body == {} or request_body==[] or request_body==None:
        return jsonify('Empty Request'),400
    person_id=request.json.get('person_id',None)
    mother_id=request.json.get('mother_id')
    father_id=request.json.get('father_id')
    if not person_id:
        return jsonify('Person_id required'),400
    doesPersonExists=Person.query.filter_by(id=person_id).first()
    if not doesPersonExists:
        return jsonify('This person doesn not exists!')
    already_assigned_relationship=PeopleRelationship.query.filter_by(person_id=person_id).first()
    if already_assigned_relationship:
        return jsonify('Already added'),400
    
    person_parents=PeopleRelationship(person_id=person_id,mother_id=mother_id,father_id=father_id)
    db.session.add(person_parents)
    db.session.commit()
    
    return jsonify(request_body),200

#------------------------GET A SPECIFIED PERSON----------------------------------------
@app.route('/person/<int:person_id>', methods=['GET'])
def get_specified_person(person_id):

    pieces_of_information={} #EVERY piece of information will be added to this one. Finally, it will be return
    
    specified_person=Person.query.filter_by(id=person_id).first()
    print(specified_person)
    if not specified_person:
        return jsonify({'msg':'This person does not exists'}),400

    pieces_of_information['personal information']=specified_person.serialize()

     # Get all relationships
    relationships=PeopleRelationship.query.all()
    all_relationships=list(map(lambda item:item.serialize(),relationships))
    # get all people
    people=Person.query.all()
    all_people=list(map(lambda person:person.serialize(),people))

    #!!!!!!!!!!!!!!!!CHILDREN!!!!!!!!!!!!!
    # child id
    children_id=[]
    parents_id=[]
    for items in all_relationships:
        if items['mother_id']!= None and items['mother_id'] == person_id:
            children_id.append(items['person_id'])
        elif items['father_id']!= None and items['father_id'] == person_id:
            children_id.append(items['person_id'])
        elif items['person_id']==person_id: ##append parent id
            parents_id.append({'mother':items['mother_id']})
            parents_id.append({'father':items['father_id']})

    children_information=[]
    for eachId in children_id:
        for person in all_people:
            if person['id'] == eachId:
                children_information.append(person)
    
    pieces_of_information['children']=children_information

    #!!!!!!!!!!!!!!!!!!! Parent !!!!!!!!!!!!!!!!!!!!!!!!!!
    parents_information={}
    for eachParentId in parents_id:
        for eachperson in all_people:
            if 'mother' in eachParentId:
                if eachParentId['mother']==eachperson['id']: ###padres
                    parents_information['mother']=eachperson
            elif 'father' in eachParentId:
                if eachParentId['father']==eachperson['id']: ###padres
                    parents_information['father']=eachperson
    pieces_of_information['parents information']=parents_information

    return jsonify(pieces_of_information),200

#---------------------------
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
