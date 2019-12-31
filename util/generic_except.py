from sanic import response

def get_except_msg(msg):
    return {"type":"error","message": msg}


def get_except_label(label):
    return {"type":"error","label": label}


def get_except(label, msg):
    return {"type":"error","label": label, "message": msg}

def get_response_error(label,e):
    return response.json(get_except(label,e),status=500)