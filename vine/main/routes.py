from flask import render_template, Blueprint, make_response, request

main = Blueprint('main', __name__)

cookie = 'lfvine'

# ---------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------- #

@main.route("/")
@main.route("/home")
@main.route("/index.html")
def index():
    ck = request.cookies.get(cookie)
    #print("------------------ before ")
    print(">>>>>>>>>>> " + str(ck) + " <<<<<<<<<<<<")
    #print("------------------ after ")

    if ck == "customer":
        return render_template('customer_tickets.html')
    elif ck == "staff":
        return render_template('staff_tickets.html')
    elif ck == "kanban":
        return render_template('kanban_tickets.html')

    return render_template('login.html')

@main.route("/login")
def login():
    return render_template('login.html')

@main.route("/customer")
def customer():
    resp = make_response(render_template('customer_tickets.html'))
    resp.set_cookie(cookie, 'customer')
    print("Cookie '" + cookie + "' set to value 'customer'") 
    return resp

@main.route("/staff")
def staff():
    resp = make_response(render_template('staff_tickets.html'))
    resp.set_cookie(cookie, 'staff')
    print("Cookie '" + cookie + "' set to value 'staff'") 
    return resp

@main.route("/kanban")
def kanban():
    resp = make_response(render_template('kanban_tickets.html'))
    resp.set_cookie(cookie, 'kanban')
    print("Cookie '" + cookie + "' set to value 'kanban'") 
    return resp

