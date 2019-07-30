from flask import Flask, request ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
from flask_cors import CORS

#Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir,"blog.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#initiliase db
db = SQLAlchemy(app)

#init Marshmallow
ma = Marshmallow(app)

# Blog Class/Model

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(50))
    email = db.Column(db.String(50))
    title = db.Column(db.String(100))
    pub_date = db.Column(db.String(30))
    blog_post = db.Column(db.Text,nullable=False)


    def __init__(self,author,email,title,pub_date,blog_post):
        self.author = author
        self.email = email
        self.title = title
        self.pub_date = pub_date
        self.blog_post =blog_post
#Product Schema

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'email', 'title', 'pub_date', 'blog_post')

# init Schema

blog_schema = BlogSchema(strict=True)
blogs_schema = BlogSchema(many=True, strict=True)



#Create route

@app.route("/blog",methods=["POST"])
def blog():
    author = request.json['author']
    email = request.json['email']
    title = request.json['title']
    pub_date = request.json['pub_date']
    blog_post = request.json['blog_post']

    new_blog = Blog(author, email, title, pub_date, blog_post)
    db.session.add(new_blog)
    db.session.commit()

    return blog_schema.jsonify(new_blog)

#get all bog details
@app.route('/blog',methods=['GET'])
def get_blogdetails():
    all_blogposts = Blog.query.all()
    result = blogs_schema.dump(all_blogposts)
    return jsonify(result.data)

#get blog by id

@app.route('/blog/<id>',methods=['GET'])
def get_blogdetail(id):
    blogposts = Blog.query.get(id)
    return  blog_schema.jsonify(blogposts)


#Update Product
@app.route("/blog/<id>",methods=["PUT"])
def update_blog(id):
    blogposts=Blog.query.get(id)
    author = request.json['author']
    email = request.json['email']
    title = request.json['title']
    pub_date = request.json['pub_date']
    blog_post = request.json['blog_post']

    blogposts.author = author
    blogposts.email= email
    blogposts.title = title
    blogposts.pub_date= pub_date
    blogposts.blog_post= blog_post



    db.session.commit()

    return blog_schema.jsonify(blogposts)



#delete product by # IDEA:

@app.route('/blog/<id>',methods=['DELETE'])
def delete_blogdetail(id):
    blogposts = Blog.query.get(id)
    db.session.delete(blogposts)
    db.session.commit()
    return  blog_schema.jsonify(blogposts)




#Run App
if __name__ == '__main__':
    app.run(debug=True)
