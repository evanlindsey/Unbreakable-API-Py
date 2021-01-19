from flask import jsonify


def json_status(status, msg, code):
    return jsonify({status: msg}), code


def success(msg):
    return json_status('message', msg, 200)


def error(msg):
    return json_status('message', msg, 400)


def auth_error(msg):
    return json_status('message', msg, 401)
