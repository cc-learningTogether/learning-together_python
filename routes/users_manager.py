from flask import Blueprint, request
from database.models.user import UserProfile
from database.db import db

users_manager_route = Blueprint("users_manager", __name__, template_folder="routes")


@users_manager_route.route('/api/data')
def data():
    query = UserProfile.query
    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            UserProfile.user_name.like(f'%{search}%'),
            UserProfile.email.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['user_name', 'email']:
            col_name = 'user_name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(UserProfile, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)
    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': UserProfile.query.count(),
        'draw': request.args.get('draw', type=int),
    }
