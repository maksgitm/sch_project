from base64 import b64encode

import flask
import qrcode
from sqlalchemy_serializer import SerializerMixin
from data import db_session
from flask import jsonify, make_response, request, abort, render_template
from data.dops import Dops
from data.make_results import get_results


blueprint = flask.Blueprint(
    'dops_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/dops')
def create_dop():
    db_sess = db_session.create_session()
    db_sess.query(Dops).delete()
    data = get_results()
    if data:
        for el in data:
            link = el['link']
            qr = qrcode.make(link)
            qr.save('static/images/test_img.jpg')
            f = open('static/images/test_img.jpg', 'rb')
            file = f.read()
            dop = Dops(
                speciality=el['topic'],
                name=el['name_'],
                cost=el['cost'],
                age=el['age'],
                qr_code=file
            )
            f.close()
            db_sess.add(dop)
            db_sess.commit()
    lst_of_qrcodes = []
    db = db_sess.query(Dops).all()
    items = [item.to_dict(only=('speciality', 'name', 'cost', 'age')) for item in db]
    codes = db_sess.query(Dops.qr_code).all()
    for n, code in enumerate(codes, 1):
        with open(f"static/qrcodes/img_{n}.jpg", 'wb') as f:
            f.write(code[0])
        f.close()
        lst_of_qrcodes.append(f"qrcodes/img_{n}.jpg")
    print(lst_of_qrcodes)
    print(items)
    return render_template('кружки.html', items=items, codes=lst_of_qrcodes, zip=zip)
# else:
#     abort(400)
