from flask import Flask, request, abort, jsonify
from gh import get_recs, similar

app = Flask(__name__)


@app.route('/api/recs', methods=['POST'])
def recs():
    if not request.json or not ('token' in request.json or 'lf' in request.json):
        abort(400)
    recs = get_recs(request.json['token'], request.json['lf'])
    return jsonify(recs), 200


@app.route('/api/similar', methods=['POST'])
def eco():
    if not request.json or not ('token' in request.json or 'repo' in request.json):
        abort(400)
    rec = similar(request.json['token'], request.json['repo'])
    return jsonify(rec), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
