from flask import Flask, render_template
from flask_restx import Api, Resource, fields

from storage_adapters.base import StorageAdapter
from storage_adapters.dao import KeyValuePair
from storage_adapters.redis_adapter import RedisAdapter
from config import settings

app = Flask(__name__)
api = Api(app, title="A tiny key-value storage Flask API")

ns = api.namespace("keys", description="Keys operations")

kvp = api.model(
    "KeyValuePair",
    {
        "key": fields.String,
        "value": fields.String,
    },
)

adapter: StorageAdapter = RedisAdapter(
    host=settings.redis_host,
    port=settings.redis_port,
).connect()


@app.route("/keys_page/", methods=["GET"])
def list_keys():
    return render_template("keys.html", items=adapter.get_all())


@ns.route("/")
class KeyList(Resource):
    @ns.marshal_list_with(kvp)
    def get(self):
        """Get all key-value pairs"""
        return adapter.get_all()

    @ns.expect(kvp)
    @ns.marshal_with(kvp, code=201)
    def post(self):
        """Create new key-value pair"""
        key = api.payload["key"]
        if adapter.key_exists(key):
            api.abort(409, f"Key {key} already exists")
        adapter.create_key(**api.payload)
        return KeyValuePair(**api.payload), 201


@ns.route("/<string:key>")
class Key(Resource):
    @ns.marshal_with(kvp)
    def get(self, key: str):
        """Get key value"""
        value = adapter.read_key(key)
        if not value:
            api.abort(404, f"Key {key} doesn't exist")
        return KeyValuePair(key=key, value=value)

    @ns.expect(kvp)
    @ns.marshal_with(kvp)
    def put(self, key: str):
        """Update key value"""
        pl = api.payload
        if not (pl and "value" in pl):
            api.abort(400, "Payload doesn't contain a value")
        value = adapter.update_key(key=key, **pl)
        if not value:
            api.abort(404, f"Key {key} doesn't exist")
        return KeyValuePair(key=key, value=value)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080,
    )
