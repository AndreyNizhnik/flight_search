from flight_search import FlightSearch
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Optional


# Initialise Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

choices = ['round', 'oneway']


class Search(FlaskForm):
    city_start = StringField( 'City from', default="Ho Chi Ming City", validators=[DataRequired("Enter city name here")])
    city_dest = StringField('City to', default="Bangkok", validators=[DataRequired("Enter city name here")])
    date_from = DateField('Start date from')
    date_to = DateField('Start date to')
    flight_type = SelectField('Flight type', choices=choices)
    rtrn_from = DateField('Return date from (for round trip only)', validators=[Optional()])
    rtrn_to = DateField('Return date to (for round trip only)', validators=[Optional()])
    adults = StringField('Number of adults (12+)', default=1, validators=[DataRequired()])
    children = StringField('Number of children (2-12)', default=0)
    infants = StringField('Number of infants (2-)', default=0)
    max_stopovers = StringField('Max number of stopovers', default=1)
    submit = SubmitField("Search Flights")


# Flask home route
@app.route("/", methods=['GET', 'POST'])
def home():
    form = Search()
    flight_search = FlightSearch()
    if form.validate_on_submit():
        fl_type = form.flight_type.data
        city_from = flight_search.get_destination_code(form.city_start.data)
        city_to = flight_search.get_destination_code(form.city_dest.data)
        if fl_type == 'oneway':
            flights = flight_search.get_flight_prices_one_way(city_from=city_from,
                                                              city_to=city_to,
                                                              city_dest=form.city_dest.data,
                                                              date_from=form.date_from.data.strftime("%d/%m/%Y"),
                                                              date_to=form.date_to.data.strftime("%d/%m/%Y"),
                                                              flight_type=form.flight_type.data,
                                                              adults=form.adults.data,
                                                              children=form.children.data,
                                                              infants=form.infants.data,
                                                              max_stopovers=form.max_stopovers.data,
                                                              )
            return render_template("flights.html", flights=flights, fl_type=fl_type)
        else:
            flights = flight_search.get_flight_prices_round(city_from=city_from,
                                                            city_to=city_to,
                                                            city_dest=form.city_dest.data,
                                                            date_from=form.date_from.data.strftime("%d/%m/%Y"),
                                                            date_to=form.date_to.data.strftime("%d/%m/%Y"),
                                                            flight_type=form.flight_type.data,
                                                            rtrn_from=form.rtrn_from.data,
                                                            rtrn_to=form.rtrn_to.data,
                                                            adults=form.adults.data,
                                                            children=form.children.data,
                                                            infants=form.infants.data,
                                                            max_stopovers=form.max_stopovers.data,
                                                            )
            return render_template("flights.html", flights=flights, fl_type=fl_type)
    else:
        return render_template("index.html", form=form)

    # for i in flights:
    #     pprint(vars(i))
    #     print("===========================")
    # print(f"Results found: {len(flights)}")


if __name__ == '__main__':
    app.run(debug=True)
