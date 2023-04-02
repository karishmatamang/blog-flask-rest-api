from datetime import datetime
from app import db
import re, random, string
from werkzeug.security import generate_password_hash, check_password_hash

def slugify(s):
    pattern=r'[^\w+]'
    return re.sub(pattern,'-',s)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),unique=True, nullable=False)
    email=db.Column(db.String(200),unique=True,nullable=False)
    password=db.Column(db.String(30))
    is_verified=db.Column(db.Boolean, default=False)    
    blogs=db.relationship('BlogModel',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.id}',{self.username}','{self.email}')"
    
    def is_authenticated(self):
        return True

    def is_active(self): # line 37
        return True
    
    def get_id(self):
        return self.id
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    
    def check_password(self, password):
        return check_password_hash(generate_password_hash(password), password)   


def get_random_string(length):
    res=''.join(random.choices(string.ascii_uppercase+string.digits,k=length))
    return res  

def generate_slug(text): 
    new_slug=slugify(text)
    if BlogModel.query.filter_by(slug=new_slug).first():
        return generate_slug(text+get_random_string(5))
    return new_slug


class BlogModel(db.Model):
    
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    title=db.Column(db.String(200), nullable=False)
    created_at= db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    updated_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow ,onupdate=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    image=db.Column(db.String(20),nullable=False,default='pic.jpg')
    slug=db.Column(db.String(250),unique=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_slug( )
        
    def get_slug(self):
        self.slug=generate_slug(self.title) 

        
    def __repr__(self) :
        return f"Post('{self.title}','{self.created_at}','{self.updated_at}','{self.slug}')"
    

blogs = [
    {
        'author': 'Martin Yanev',
        'title': 'Post 1',
        'content': 'Software engineering',
        'created_at': 'March 05, 2022',
        'updated_at': 'March 05, 2022'
        
    },
    {
        'author': 'Will Smith',
        'title': 'Post 2',
        'content': 'Aerospace Content',
        'created_at': 'January 01, 2022',
        'updated_at': 'March 05, 2022'

    },
    {
        'author': 'Lucy Lawless',
        'title': 'Post 3',
        'content': 'Fashion',
        'created_at': 'December 05, 2021',
        'updated_at': 'March 05, 2022'

    }
]

