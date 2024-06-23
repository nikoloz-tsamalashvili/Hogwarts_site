from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hghphghp'


app.config['SQLALCHEMY_BINDS'] = {
    'spells': 'sqlite:///hp_spells.db',
    'characters': 'sqlite:///hp_students.db'
}

db = SQLAlchemy(app)


class Spells(db.Model):
    __bind_key__ = 'spells'
    id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.String)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(3000), unique=True, nullable=False)


class SpellForm(FlaskForm):
    name = StringField('Spell Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Spell')


class Characters(db.Model):
    __bind_key__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    house = db.Column(db.String(100))
    dateOfBirth = db.Column(db.String(100))  # Change this if dateOfBirth is a string
    ancestry = db.Column(db.String(100))
    wand = db.Column(db.String(100))
    patronus = db.Column(db.String(100))
    image = db.Column(db.String(100))

    def __str__(self):
        return (f'name {self.name}, species {self.species}, gender {self.gender}, house {self.house}, '
                f'dateOfBirth {self.dateOfBirth}, ancestry {self.ancestry}, wand {self.wand}, '
                f'patronus {self.patronus}, image {self.image}')


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/Spells', methods=['GET', 'POST'])
def spells_view():
    form = SpellForm()
    if form.validate_on_submit():
        new_spell = Spells(name=form.name.data, description=form.description.data)
        try:
            db.session.add(new_spell)
            db.session.commit()
            flash('Spell added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding spell: ' + str(e), 'danger')
        return redirect(url_for('spells_view'))

    all_spells = Spells.query.all()
    return render_template('spells.html', all_spells=all_spells, form=form)


@app.route('/Gryffindor')
def gryffindor():
    return render_template("Gryffindor.html")

@app.route('/Slytherin')
def slytherin():
    return render_template("Slytherin.html")

@app.route('/Hufflepuff')
def hufflepuff():
    return render_template('Hufflepuff.html')


@app.route('/Ravenclaw')
def ravenclaw():
    return render_template('Ravenclaw.html')


@app.route('/Search', methods=['POST', 'GET'])
def Search():
    if request.method == 'POST':
        stu = request.form['student']
        session['student'] = stu
        return redirect(url_for('Results'))
    return render_template('Search.html')


@app.route('/Results')
def Results():
    info = Characters.query.filter_by(name=session['student']).all()
    session.pop('student', None)
    return render_template('Results.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)



