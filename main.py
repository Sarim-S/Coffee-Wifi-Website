from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g 5:30PM', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()], choices=[("✘"),("☕️"), ("☕️☕️"), ("☕️☕️☕️"), ("☕️☕️☕️☕️"), ("☕️☕️☕️☕️☕️")])
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=[("✘"),("💪"), ("💪💪"), ("💪💪💪"), ("💪💪💪💪"), ("💪💪💪💪💪")])
    power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=[("✘"), ("🔌"), ("🔌🔌"), ("🔌🔌🔌"), ("🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌")])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

def ends_in_new_line(file_path):
    with open(file_path, mode="r", newline="") as file:

        file.seek(0, 2)
        file_size = file.tell()

        if file_size == 0:
            return False

        file.seek(file_size - 1)
        last_char = file.read(1)

        return last_char == "\n"
    
# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        new_cafe_data = []
        for values in form.data.values():
            new_cafe_data.append(values)

        formatted_data = new_cafe_data[:7]
        with open('cafe-data.csv', mode="a", newline="", encoding="utf-8") as file:
            if not ends_in_new_line('cafe-data.csv'):
                file.write("\n")
            writer = csv.writer(file)
            writer.writerow(formatted_data)
            
        
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
