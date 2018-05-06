from flask import render_template, request, jsonify
from . import main
from ..models import Item, CoaSummaryView
import datetime
from .. import db

@main.route('/')
def index():
    for row in CoaSummaryView.query.all():
        print(row.site_name)
    return render_template('index.html')

@main.route('/sitecategoriesbreakdown')
def site_details():
    site_name = 'Union Beach'
    start_date = datetime.datetime(2016, 1 ,1)
    end_date = datetime.datetime(2016, 12, 31)
    print (site_name)
    result = CoaSummaryView.query.filter(CoaSummaryView.site_name == site_name, \
                                           CoaSummaryView.volunteer_date > start_date,
                                           CoaSummaryView.volunteer_date < end_date). \
                                           with_entities(CoaSummaryView.material, \
                                           db.func.sum(CoaSummaryView.quantity)). \
                                           group_by(CoaSummaryView.material)
    for row in result:
       print(row)
    return jsonify(result)

