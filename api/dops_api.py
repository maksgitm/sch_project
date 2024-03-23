import flask
import qrcode

from data import db_session
from flask import jsonify, make_response, request, abort
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
        return jsonify({'success': 'ok'})
    else:
        abort(400)
