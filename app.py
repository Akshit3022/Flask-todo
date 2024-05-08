from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
db = SQLAlchemy(app)

class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(400), nullable=False)


# with app.app_context():
#     db.create_all()


# class HelloWorld(Resource):
#     def get(self):
#         return {'data': 'Hello world!'}
    
# class HelloName(Resource):
#     def get(self, name):
#         return {'data': 'Hello {}!'.format(name)} 

# api.add_resource(HelloWorld, '/helloworld')
# api.add_resource(HelloName, '/helloname/<string:name>')    

# todos = {
#     1: {'tasks':'1 : Write a program', 'summary':'Write it using python'},
#     2: {'tasks':'2 : Write a program', 'summary':'Write it using python'},
#     3: {'tasks':'3 : Write a program', 'summary':'Write it using python'}
# }

task_args = reqparse.RequestParser()
task_args.add_argument('task', type=str, required=True, help='No task provided')
task_args.add_argument('summary', type=str, required=True, help='No summary provided')

task_update_args = reqparse.RequestParser()
task_update_args.add_argument('task', type=str)
task_update_args.add_argument('summary', type=str)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String,
}

# class ToDoList(Resource):
#     @marshal_with(resource_fields)
#     def get(self):
#         return todos

class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        todo = ToDoModel.query.filter_by(id=todo_id).first()
        if todo:
            abort(409, "Could not find task with that id")
        return todo

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, "Task already exists")
        
        todo = ToDoModel(id=todo_id, task=args['task'], summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    
    @marshal_with(resource_fields)
    def patch(self, todo_id):
        args = task_update_args.parse_args()
        todo = ToDoModel.query.filter_by(id=todo_id).first()

        if todo:
            abort(409, "Task Not Found")
        
        if args['task']:
            todo.task = args['task']

        if args['summary']:    
            todo.summary = args['summary']

        db.session.commit()
        return todo
    
    def delete(self, todo_id):
        todo = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(todo)

        return "Deleted successfully"

api.add_resource(ToDo, '/todo/<int:todo_id>')
# api.add_resource(ToDoList, '/todo-list')


if __name__ == '__main__':
    app.run(debug=True)
