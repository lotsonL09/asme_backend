

def scheme_user(user_row):
    return {
        'id_user':user_row[0],
        'dni':user_row[1],
        'first_name':user_row[2],
        'last_name':user_row[3],
        'team_name':user_row[4],
        'area_name':user_row[5]
    }

def scheme_ticket(ticket_row):
    try:
        return {
            "id_ticket":ticket_row[0],
            "number_ticket":ticket_row[1],
            "first_name":ticket_row[2],
            "last_name":ticket_row[3],
            "DNI":ticket_row[4],
            "email":ticket_row[5],
            "cell_phone":ticket_row[6],
            "booking_time":ticket_row[7]
        }
    except:
        return {
            "id_ticket":ticket_row[0],
            "number_ticket":ticket_row[1],
            "first_name":None,
            "last_name":None,
            "DNI":None,
            "email":None,
            "cell_phone":None,
            "booking_time":None
        }