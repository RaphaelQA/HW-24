import os
from typing import Union, Iterable

from flask import Flask, request, jsonify, Response
from marshmallow import ValidationError

from bulider import build_query
from models import RequestSchema

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query() -> Union[Response, tuple[Response, int]]:
    data = request.json
    try:
        RequestSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400
    first_result: Iterable[str] = build_query(
        cmd=data['cmd1'],
        value=data['value1'],
        file_name=data['file_name'],
        data=None
    )
    second_result: Iterable[str] = build_query(
        cmd=data['cmd1'],
        value=data['value1'],
        file_name=data['file_name'],
        data=first_result
    )
    return jsonify(second_result)
