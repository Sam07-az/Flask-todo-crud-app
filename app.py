from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

 
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)





# '''this was for just practice purpose while we were studing for A2'''
# from flask import Flask, request

# app = Flask(__name__)

# @app.after_request
# def after_request_func(response):
#     print('After Request')
#     print(response)
#     # Modify the response or perform cleanup operations here
#     return response

# @app.route('/')
# def index():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# app = Flask(__name__)

# # Set up JWT
# app.config["JWT_SECRET_KEY"] = "super-secret-key"
# jwt = JWTManager(app)

# # Dummy user data for demo purposes
# users = {
#     "john": "password",
#     "jane": "password",
# }

# # Login route
# @app.route("/login", methods=["POST"])
# def login():
#     username = request.json.get("username")
#     password = request.json.get("password")
#     if not username or not password:
#         return jsonify({"msg": "Missing username or password"}), 400
#     if username not in users or users[username] != password:
#         return jsonify({"msg": "Invalid username or password"}), 401
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token)

# # Protected route
# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

# if __name__ == "__main__":
#     app.run()
