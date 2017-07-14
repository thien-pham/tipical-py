import json
from flask import request, Response, url_for, flash
from jsonschema import validate, ValidationError
from flask_login import login_user, login_required, current_user, logout_user

# from . import models
from . import decorators
from tips import app
from .database import session, Tip, User

# JSON Schema describing the structure of a tip
tip_schema = {
    "properties": {
        "title" : {"type" : "string"},
        "body": {"type": "string"}
        # "location": {"type": "geography"}
    },
    "required": ["title", "body"]
}

@app.route("/api/tips", methods=["GET"])
@decorators.accept("application/json")
def tips_get():
    """ Get a list of tips """
     # Get the posts from the database
    tips = session.query(Tip).order_by(Tip.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([tip.as_dictionary() for tip in tips])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/tips/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def tip_get(id):
    """ Single tip endpoint """
    # Get the tip from the database
    tip = session.query(Tip).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not tip:
        message = "Could not find tip with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(tip.as_dictionary())
    return Response(data, 200, mimetype="application/json")


@app.route("/api/tips", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
@login_required
def post_tip():
    """ Add a new tip """
    data = request.json

    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity TODO: get rid of validation
    # try:
    #     validate(data, tip_schema)
    # except ValidationError as error:
    #     data = {"message": error.message}
    #     return Response(json.dumps(data), 422, mimetype="application/json")

    # Add the tip to the database
    tip = Tip(title=data["title"], body=data["body"], author=current_user)
    session.add(tip)
    session.commit()

    # Return a 201 Created, containing the tip as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(tip.as_dictionary())
    headers = {"Location": url_for("tip_get", id=tip.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")

# endpoint which receives a PUT request at /api/post/<id

@app.route("/api/tips/<int:id>", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
@login_required
def update_tip(id):
    """update a single tip"""

    tip = session.query(Tip).get(id)
    data = request.json
    # try:
    #     validate(data, tip_schema)
    # except ValidationError as error:
    #     data = {"messae": error.message}
    #     return Response(json.dumps(data), 422, mimetype="application/json")

# TODO: Allow partial (single-field) updates
    tip.title = data["title"]
    tip.body = data["body"]
    # tip.location = data["location"]
    session.commit()

    data = json.dumps(tip.as_dictionary())
    headers = {"Location": url_for("tip_get", id=tip.id)}
    return Response(data, 200, headers=headers, mimetype="application/json")

# endpoint for deleting a single post
@app.route("/api/tips/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def delete_tip(id):
    """delete a single tip"""

    tip = session.query(Tip).get(id)
    session.delete(tip)
    session.commit()

    message = "Successfully deleted tip with id {}".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")
    # return redirect(url_for("tips"))
