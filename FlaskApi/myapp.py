from flask import request, url_for, jsonify, Flask, make_response
import flask

app = Flask(__name__)

reminder = [
    {
    'id': 0,
    'title': 'Bhuuk Lagi Hai',
    'datetime': '2020-08-22-14:00',
    'description': 'Bhuuk toh bhuuk hoti hai isme description kya du'
    }
]


# A route to return all of the available entries in our catalog.
@app.route('/all', methods=['GET'])
def home_api():
    return jsonify(reminder)

@app.route('/one', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for alarm in reminder:
        if alarm['id'] == id:
            results.append(alarm)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/post', methods=['POST'])
def create_alarm():
    if not request.json or not 'title' in request.json or not 'datetime' in request.json:
        abort(400)
    alarm = {
        'id': reminder[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'datetime': request.json.get('datetime'),
    }
    reminder.append(alarm)
    return jsonify({'alarm': alarm}), 201

@app.route('/<int:task_id>', methods=['PUT'])
def update_task(alarm_id):
    alarm = [alarm for alarm in reminder if reminder['id'] == alarm_id]
    if len(alarm) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'datetime' in request.json and type(request.json['datetime']) != unicode:
        abort(400)
    alarm[0]['title'] = request.json.get('title', alarm[0]['title'])
    alarm[0]['description'] = request.json.get('description', alarm[0]['description'])
    alarm[0]['datetime'] = request.json.get('done', alarm[0]['done'])
    return jsonify({'alarm': alarm[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    alarm = [alarm for alarm in reminder if reminder['id'] == alarm_id]
    if len(task) == 0:
        abort(404)
    reminder.remove(alarm[0])
    return jsonify({'result': True})


app.run()