from pymongo import DESCENDING, ASCENDING
from QUANTAXIS.QAUtil import DATABASE
"""对于POSITION的增删改查
"""


def save_position(message, collection=DATABASE.positions):
    """save account

    Arguments:
        message {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})
    """
    try:
        collection.create_index(
            [("account_cookie", ASCENDING), ("position_id", ASCENDING)], unique=True)
    except:
        pass
    collection.update(
        {'account_cookie': message['account_cookie'], 'position_id': message['position_id'],
        {'$set': message},
        upsert=True
    )
