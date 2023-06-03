from flask import jsonify, make_response

def success(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res), 200)

def badRequest(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res), 400)

def notFound(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res), 404)

def serverError(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res), 500)