from flask import Flask, jsonify
app = Flask(__name__)

configs = [
    {
        "name": "Calsoft",
        "description": "Ubuntu OS System",
        "ip": "172.23.106.217",
        "active": True,
        "location": "Alten Calsoft Labs",
        "updated": True
    }
]


@app.route('/', methods=['GET'])
def main_page():
    return jsonify("This is a simple RESTful app.")


@app.route('/configs', methods=['GET'])
def list():
    return jsonify(configs)


from flask import abort


@app.route('/configs/<string:feature>', methods=['GET'])
def get_config(feature):

    if feature != "sysconfig":
        abort(404)
    elif not len(configs):
        abort(404)
    else:
        sysconfig = configs[0]
        return jsonify(sysconfig)


from flask import make_response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_input(error):
    return make_response(jsonify({'error': 'Bad input'}), 400)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
