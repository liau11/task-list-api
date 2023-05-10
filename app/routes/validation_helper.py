from flask import abort, make_response


def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid id '{id}'"}, 400))

    item = model.query.get(id)

    if not item:
        abort(make_response({"message": f"{model.__name__} {id} not found"}, 404))

    return item
