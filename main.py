from flask import Flask, jsonify
import redis
import time

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/data/<key>')
def get_data(key):
    # Vérifie si la donnée est dans Redis
    cached_data = r.get(key)
    if cached_data:
        return jsonify({"data": cached_data.decode('utf-8'), "source": "cache"})

    # Simule une réponse lente
    time.sleep(2)
    data = f"value for {key}"
    # Stocke la donnée dans Redis avec une durée de vie de 60 secondes
    r.setex(key, 60, data)
    return jsonify({"data": data, "source": "database"})

if __name__ == '__main__':
    app.run(debug=True)
