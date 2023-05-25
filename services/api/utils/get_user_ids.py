def get_user_ids(info):
    temp_user_id = info.context.get('request').cookies.get('tempId')
    user_id = info.context.get('user_id')
    return temp_user_id, user_id
