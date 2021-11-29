import collections
from flask_restful import Resource, marshal_with, fields, reqparse
from .models import User
from . import db
from .validation import NotFoundError, BusinessValidationError

output_card_field = {
    "id" : fields.Integer, 
    "date" : fields.DateTime,
    "question" : fields.String, 
    "answer" :fields.Integer,
    "collection_id" :fields.String

}

output_collection_field = {
    "id" : fields.Integer, 
    "date" : fields.DateTime,
    "name" : fields.String, 
    "user_id" :fields.Integer,
    "cards" :fields.Nested(output_card_field)
}


output_user_fields = {
    "id" : fields.Integer,
    "email" : fields.String,
    "first_name" : fields.String,
    "collections" : fields.Nested(output_collection_field)

}


create_user_parser  = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')


update_user_parser  = reqparse.RequestParser()
update_user_parser.add_argument('email')

class UserAPI(Resource):
    @marshal_with(output_user_fields)
    def get(self, id):
       
        user = db.session.query(User).filter(User.id == id).first()
        if user:
            return user,200
        else:
            raise NotFoundError(status_code = 404)

    @marshal_with(output_user_fields)
    def put(self, id):
        args = update_user_parser.parse_args()
        email = args.get("email", None)

        if email is None:
            raise BusinessValidationError (Status_code = 400, error_code = "BE1002", error_message = "email is required")

        user =  db.session.query(User).filter(User.email == email).first()   

        if user: 
            raise BusinessValidationError (Status_code = 400, error_code = "BE1004", error_message = "Duplicate user")
      
        
        #check if the user exists 
        user = db.session.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundError(status_code=404)
        user.email = email  
        db.session.add(user)
        db.session.commit()
        return user    

    def delete(self, id):
        #check if the user exists 
        user = db.session.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundError(status_code=404)
             

        #check if there are articles for this user 
        #throw an error 
        if len(user.collections ) > 0 :
            BusinessValidationError (Status_code = 400, error_code = "BE1005", error_message = "articles are present for this user") 

        #if there is no dependency 
        #delete error
        db.session.delete(user)
        db.session.commit()

        return "", 200




    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username" , None)
        email = args.get("email", None)

        if username is None: 
            raise BusinessValidationError (Status_code = 400, error_code = "BE1001", error_message = "username is required")

        if email is None:
            raise BusinessValidationError (Status_code = 400, error_code = "BE1002", error_message = "email is required")

        user =  db.session.query(User).filter((User.username == username) |( User.email == email)).first()   

        if user: 
            raise BusinessValidationError (Status_code = 400, error_code = "BE1004", error_message = "Duplicate user")

        new_user =  User(username = username , email = email)
        db.session.add(new_user)
        db.session.commit()
        return "",201     

        




class CollectionAPI(Resource):
    def get(self, id):
        print("get" , id)
        return {"id" : id}

    def put(self, id):
        print("put" , id)
        return {"id" : id}

    def delete(self, id):
        print("delete" , id)
        return {"id" : id}

    def post(self):
        print("post")
        return {"action" : "post" }



class CardAPI(Resource):
    def get(self, id):
        print("get" , id)
        return {"id" : id}

    def put(self, id):
        print("put" , id)
        return {"id" : id}

    def delete(self, id):
        print("delete" , id)
        return {"id" : id}

    def post(self):
        print("post")
        return {"action" : "post" }    