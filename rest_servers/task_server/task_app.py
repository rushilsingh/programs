from flask import Flask, jsonify
app = Flask(__name__)

tasks = [
    {
        'id': "1234",
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit',
        'done': False,
        'importance': 'low',
        'location': 'market',
        'person': 'bob'
    },
    {
        'id': "1235",
        'title': u'Learn REST',
        'description': u'Need to find a good REST tutorial on the web',
        'done':False,
        'importance': 'medium',
        'location': 'work',
        'person': 'rushil'

    },
    {    'id':"1236",
         'title': u'Relax',
         'description': u'Need to learn to relax.',
         'done':False,
         'importance': 'high',
         'location': 'everywhere',
         'person': 'rushil'
    }
]

@app.route('/', methods = ['GET'])
def main_page():
   return jsonify("This is a simple RESTful app.")


@app.route('/tasks', methods = ['GET'])
def get_tasks():
    return jsonify(tasks)

from flask import abort

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not len(task):
        abort(404)
    return jsonify(task[0])

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

@app.errorhandler(400)
def bad_input(error):
    return make_response(jsonify({'error':'Bad input'}), 400)

@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error':'Method not allowed'}), 405)

from flask import request

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    if not len(tasks):
        task = {
                   'id':"1234",
                   'title': request.json['title'],
                   'description': request.json.get('description', ""),
                   'done': request.json.get('done', False),
                   'importance': request.json.get('importance', 'low'),
                   'location': request.json.get('location', 'everywhere'),
                   'person': request.json.get('person', 'rushil')
               }
    else:
        id = str(int(tasks[-1]['id']) + 1)
        task = {
                   'id':id,
                   'title': request.json['title'],
                   'description': request.json.get('description', ""),
                   'done': request.json.get('done', False),
                   'importance': request.json.get('importance', 'low'),
                   'location': request.json.get('location', 'everywhere'),
                   'person': request.json.get('person', 'rushil')

               }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<string:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not len(task):
        abort(404)
    if not request.json:
        abort(400)

    for key in request.json:
        task[0][key] = request.json.get(key, task[0][key])

    return jsonify(task[0])

@app.route('/tasks/<string:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not len(task): abort(404)
    tasks.remove(task[0])
    return jsonify({"result":True})

@app.route('/tasks', methods = ['DELETE'])
def delete_all():
    while(len(tasks)): tasks.pop()
    return jsonify({'result':True})


if  __name__ == '__main__':
   app.run(debug=True, host = "0.0.0.0")
