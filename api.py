import json

from flask import Flask, abort, request, render_template
from graphql import graphql_sync
from graphql.error import format_error

# TODO: validate schema
from app import schema

app = Flask(__name__)


# TODO: refactor to class-based view
@app.route('/', methods=['GET', 'POST'])
def query():
    # TODO: lock the playground behind debug mode
    if "text/html" == request.accept_mimetypes.best:
        return render_template("playground.html")

    try:
        graphql_query = request.json["query"]
        variables = request.json.get("variables")
        operation_name = request.json.get("operationName")
    except KeyError:
        abort(400, "No GraphQL query found in the request")

    context = {"request": request}

    result = graphql_sync(
        schema,
        graphql_query,
        root_value=None,
        variable_values=variables,
        context_value=context,
        operation_name=operation_name,
    )

    response_data = {"data": result.data}

    if result.errors:
        response_data["errors"] = [
            format_error(err) for err in result.errors
        ]

    return response_data
