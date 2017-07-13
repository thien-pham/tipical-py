import json

from flask import request, Response, url_for, render_template
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session

# JSON Schema describing the structure of a tip
tip_schema = {
    "properties": {
        "title" : {"type" : "string"},
        "body": {"type": "string"}
    },
    "required": ["title", "body"]
}

@app.route("/api/tips", methods=["GET"])
@decorators.accept("application/json")
def tips_get():
    """ Get a list of tips """
     # Get the posts from the database
    tips = session.query(models.Tip).order_by(models.Tip.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([tip.as_dictionary() for tip in tips])
    return Response(data, 200, mimetype="application/json", render_template("tips.html"))

@app.route("/api/tips/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def tip_get(id):
    """ Single tip endpoint """
    # Get the tip from the database
    tip = session.query(models.Tip).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not tip:
        message = "Could not find tip with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(tip.as_dictionary())
    return Response(data, 200, mimetype="application/json", render_template("tip.html"))


@app.route("/api/tips", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_tip():
    """ Add a new tip """
    data = request.json

    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity
    try:
        validate(data, tip_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # Add the tip to the database
    tip = models.Tip(title=data["title"], body=data["body"])
    session.add(tip)
    session.commit()

    # Return a 201 Created, containing the tip as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(tip.as_dictionary())
    headers = {"Location": url_for("tip_get", id=tip.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json", render_template("add_tip.html"))

# endpoint which receives a PUT request at /api/post/<id>
@app.route("/api/tips/<int:id>/edit", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def update_tip(id):
    """update a single tip"""

    tip = session.query(models.Tip).get(id)
    data = request.json
    try:
        validate(data, tip_schema)
    except ValidationError as error:
        data = {"messae": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    tip.title = data["title"]
    tip.body = data["body"]
    session.commit()

    data = json.dumps(tip.as_dictionary())
    headers = {"Location": url_for("tip_get", id=tip.id)}
    return Response(data, 200, headers=headers, mimetype="application/json",
                    render_template("edit_tip.html"))

# endpoint for deleting a single post
@app.route("/api/tips/<int:id>/delete", methods=["DELETE"])
@decorators.accept("application/json")
def delete_tip(id):
    """delete a single tip"""

    tip = session.query(models.Tip).get(id)
    session.delete(tip)
    session.commit()

    message = "Successfully deleted tip with id {}".format(id)
    data = json.dumps({"message": message})
    return Response(data, 200, mimetype="application/json")
    # return redirect(url_for("tips"))
