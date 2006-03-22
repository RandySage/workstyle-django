def get_id_list_from_url(s) :
    id_list = []
    if s == None or s == "":
        return id_list
    s_id_list = s.split('-')
    for id in s_id_list :
        try :
            if int(id) > 0 :
                id_list.append(int(id))
        except ValueError :
            pass
    return id_list

