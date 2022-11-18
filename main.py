from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import Form, TextAreaField, StringField
from wtforms.validators import InputRequired, Length
from deta import Deta
from datetime import datetime


class PasteForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=3, max=100)])
    content = TextAreaField('Content',
                                validators=[InputRequired()])


# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah1blah2bla314'
deta = Deta() 
db = deta.Base('binDB')  # access your DB


@app.route('/')
def index():
    res = db.fetch()

    bins = res.items
    # fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        bins += res.items

    return render_template('index.html', bins=bins)


@app.route('/form', methods=('GET', 'POST'))
def newbin():
    form = PasteForm()
    if form.validate_on_submit():
        db.put({
            "title": form.title.data,
            "content": form.content.data,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        return redirect(url_for('index'))
    return render_template('newbin.html', form=form)

@app.route("/bin/<key>")
def show_bin(key):
    bin = db.get(key)
    if bin:
        return render_template('bin.html', bin=bin)
    else:
        return render_template('bin.html', bin={"title": "No found", "content": "not found"})


# @app.route("/api/bins/<key>")
# def get_bin(key):
#     bin = db.get(key)
#     return bin if bin else jsonify({"error": "Not found"}, 404)