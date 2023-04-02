from flask import request
import os
from flask import Response,json
from flask_restful import Resource, abort,fields,marshal_with
from models import *
from flask_login import login_user,current_user
from werkzeug.utils import secure_filename
from app import login_manager
from app import app, allowed_file
from models import *
from datetime import datetime

resource_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'content': fields.String,
	'user_id': fields.String,
    'slug':fields.String,
    'image':fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime

}

class BlogApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        blog=BlogModel.query.all()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 6, type=int)
        pages = BlogModel.query.paginate(page=page, per_page=per_page)
        blogs=pages.items
        return blogs

class ListBlog(Resource):
    @marshal_with(resource_fields)
    def get(self):
        user_id=current_user.id
        user=User.query.filter_by(id=user_id).first()
        blogs=BlogModel.query.filter_by(user_id=user.username).all()
        return(blogs)

class BlogDetail(Resource):
    @marshal_with(resource_fields)
    def get(self,slug):
        blogs=BlogModel.query.filter_by(slug=slug).first()
        print(blogs)
        return blogs
    
class BlogDelete(Resource):
    @marshal_with(resource_fields)   
    def delete(self,slug):
        response={} 
        blog=BlogModel.query.filter_by(slug=slug).first()
        print(blog.slug)
        # blog.delete()
        db.session.delete(blog)
        db.session.commit()
        response["status"] = 204
        response["message"] = "User deleted successfully"
        return response 

# def convert_and_save(image):
#         data_as_dictionary = json.loads(json.loads(image.decode('utf-8')))
#         base64_img = data_as_dictionary['image']
#         bytes_img = encode(base64_img, 'utf-8')
#         binary_img = base64.decodebytes(bytes_img)
#         with open("imageToSave.jpg", "wb") as fh:
#            fh.write(binary_img)


class AddBlog(Resource):
    
    def post(self):
        response={}
        response['status']=500
        response['message']='Something went wrong'   
        try:            
            data = request.get_json()
            title=data.get('title')
            content=data.get('content')
            user_id=current_user.id  
            file=request.files.get('image')
            print(file)      
            # file = convert_and_save(image)
            # print(file)
            user=User.query.filter_by(id=user_id).first()
            print(content)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                 response['message']='image not uplaoded'   
            blog= BlogModel(user_id=user.username,title=title, content=content,image=file) 
            db.session.add(blog)
            db.session.commit()
            response['status']=200
            response['message']='blog created'

        except Exception as e:
            print(e)

        return response


class UpdateBlog(Resource):
    def put(self,slug):
        response={}
        response['status']=500
        response['message']='Something went wrong'  
        blog=BlogModel.query.filter_by(slug=slug).first()
        try:            
            data = request.get_json()
            title=data.get('title')
            content=data.get('content')
            file=request.files.get('image')          
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            # blog.title=title
            # blog.content=content
            # blog.image=file
            updateblog=BlogModel.query.filter_by(slug=slug).update(dict(title=title,content=content,image=blog.image,updated_at=datetime.now()))
            db.session.commit()
            response['status']=200
            response['message']='blog updated'

        except Exception as e:
            print(e)

        return response

class Login(Resource):
    def post(self):
        response={}
        response['status']=500
        response['message']='Something went wrong'
        try:
            data=request.get_json()

            if data.get('email') is None:
                response['message']='key email not found'
                raise Exception('key email not found')

            if data.get('password') is None:
                response['message']='key password not found'
                raise Exception ('key password not found')
            
            check_user=User.query.filter_by(email=data.get('email')).first()
            if check_user is None:
                response['message']='invalid email or user not found'
                raise Exception ('invalid email or user not found')
            
            if check_user and check_user.check_password(data.get('password')):  
                login_user(check_user)        
                response['status']=200
                response['message']='welcome'
            else:
                response['message']='invalid password '
                raise Exception ('invald password')
        except Exception as e:
            print(e)

        return response


class Register(Resource): 
    def post(self):
        response={}
        response['status']=500
        response['message']='Something went wrong'      
        try:
            data = request.get_json()
            if data.get('username') is None:
                response['message']='key username not found'
                raise Exception('key username not found')

            if data.get('email') is None:
                response['message']='key email not found'
                raise Exception('key eamil not found')

            if data.get('password') is None:
                response['message']='key password not found'
                raise Exception ('key password not found')
            
            check_user=User.query.filter_by(email=data.get('email')).first()
            if check_user:
                response['message']='email already taken'
                raise Exception ('email already taken')
            
            password=data.get('password')
            user = User(username=data.get('username'), email=data.get('email'),is_verified=True) 
            user.set_password(password)  
            print(user.password)
            db.session.add(user)
            db.session.commit()
            response['status']=200
            response['message']='User created'

        except Exception as e:
            print(e)

        return response
    


            
