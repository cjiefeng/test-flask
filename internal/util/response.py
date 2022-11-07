from flask import make_response, jsonify


def bad_response(error):
    result = {
        'errors': error
    }
    return make_response(jsonify(result), 400)


def success_response(result):
    return make_response(jsonify(result), 200)
