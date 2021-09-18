from flask import Flask, request, abort, jsonify

from gh import get_recs

app = Flask(__name__)

@app.route('/api/recs', methods=['POST'])
def create_task():
    if not request.json or not 'token' in request.json:
        abort(400)
    recs = get_recs(request.json['token'], request.json['lf'])
    return jsonify(recs), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)