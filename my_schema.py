from schema import Schema, And, Or, Optional, Use

product_schema = Schema({'product': str, 'quantity': And(Use(int), lambda n: n > 0),
                         Optional('price'): Use(float)}, ignore_extra_keys=True)

customer_schema = Schema({'fname': str, 'lname': str, 'email': str, 'login': str,
                          'password': And(str, lambda s: len(s) > 6)}, ignore_extra_keys=True)

login_schema = Schema({'login': str, 'password': str})
