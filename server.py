import os
from api import dops_api
from flask import Flask, render_template, url_for, make_response, jsonify
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_puper_secret_key_you_will_not_get_it'


def main():
    db_session.global_init("db/sch_1357_db.sqlite")
    app.register_blueprint(dops_api.blueprint)
    # app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'ERROR': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def start():
    return render_template("сайт.html", title='Школа 1357')


@app.route('/кружки')
def show_1():
    return render_template('кружки.html', title='Школа 1357')


if __name__ == '__main__':
    main()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
