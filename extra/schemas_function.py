

def scheme_user(user_row):
    return {
        'id_user':user_row[0],
        'dni':user_row[1],
        'first_name':user_row[2],
        'last_name':user_row[3],
        'team_name':user_row[4],
        'area_name':user_row[5]
    }