from flask import Flask,render_template,redirect
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import logout_user,LoginManager

app=Flask(__name__)
app.config.from_object(Config)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'very secret'
CSRFProtect(app)
api = Api(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from api import *

@login_manager.user_loader
def load_user(user):
    user=User.query.get(int(user))
    return user

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    pages = BlogModel.query.paginate(page=page, per_page=per_page)
    return render_template('home.html',pages=pages)
api.add_resource(BlogApi,'/view')

@app.route('/addblog')
def addblog():
    return render_template('addblog.html')
api.add_resource(AddBlog,'/api/addblog',endpoint='addblog-api')

@app.route('/listblog',endpoint='listblog')
def listblog():
     return render_template('listblog.html')
api.add_resource(ListBlog,'/api/listblog',endpoint='listblog-api')

@app.route('/blogdetail/<slug>')
def blogdetail(slug):
     print(slug)
     slug=slug
     return render_template('blogdetail.html',slug=slug)
api.add_resource(BlogDetail,'/api/blogdetail/<slug>/',endpoint='blogdetail-api')

@app.route('/updateblog/<slug>')
def updateblog(slug):
     blog=BlogModel.query.filter_by(slug=slug).first()
     print(blog.content)
     return render_template('updateblog.html',blog=blog)
api.add_resource(UpdateBlog,'/api/updateblog/<slug>',endpoint='updateblog-api')

api.add_resource(BlogDelete,'/api/blogdelete/<slug>',endpoint='blogdelete-api')

@app.route('/login')
def login():
      return  render_template('login.html')
api.add_resource(Login,'/api/login',endpoint='login-api')

@app.route('/register', endpoint='register')
def register():
      return  render_template('register.html')
api.add_resource(Register,'/api/register', endpoint='register-api')

@app.route('/logout')
def logout():
    logout_user()    
    return redirect('/login')

api.init_app(app)
