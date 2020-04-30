from django.contrib.auth.decorators import login_required, user_passes_test


tech_login_required = user_passes_test(lambda u: True if u.is_technician else False, login_url='/error/')


def technician_login_required(view_func):
    decorated_view_func = login_required(tech_login_required(view_func), login_url='/error/')
    return decorated_view_func


cust_login_required = user_passes_test(lambda u: True if u.is_customer else False,
                                       login_url='/error/')

# to allow admin
# False if u.is_technician else True


def customer_login_required(view_func):
    decorated_view_func = login_required(cust_login_required(view_func), login_url='/error/')
    return decorated_view_func


adm_login_required = user_passes_test(
    lambda u: True if not u.is_customer and not u.is_technician else False, login_url='/error/')


def admin_login_required(view_func):
    decorated_view_func = login_required(adm_login_required(view_func), login_url='/error/')
    return decorated_view_func

