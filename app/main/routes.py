from flask import render_template, request, jsonify
from . import main
from ..models import Item, CoaSummaryView
import datetime
from .. import db
from collections import OrderedDict

@main.route('/')
def index():
    #for row in CoaSummaryView.query.all():
    #    print(row.site_name)
    return render_template('index.html')

@main.route('/sitecategoriesbreakdown')
def site_details():
    location_category = request.args.get('locationCategory', 
                                          default = 'site', type = str)
    site_id = request.args.get('siteId',default = 0, type = int)
    location_name = request.args.get('locationName',
                                 default = 'Union Beach', type = str)
    site_name = 'Union Beach'
    start_date = datetime.datetime(2016, 1 ,1)
    end_date = datetime.datetime(2016, 12, 31)
    
    result = CoaSummaryView.query \
        .filter(
            CoaSummaryView.site_name == site_name, \
            CoaSummaryView.volunteer_date > start_date,
            CoaSummaryView.volunteer_date < end_date) \
        .with_entities(
            CoaSummaryView.material, \
            db.func.sum(CoaSummaryView.quantity)) \
        .group_by(CoaSummaryView.material)

    return jsonify(result)

@main.route('/getsitesdropdownlist')
def site_list():
    sql_result = CoaSummaryView.query \
        .filter() \
        .with_entities(CoaSummaryView.site_name) \
        .group_by(CoaSummaryView.site_name) \
        .order_by(CoaSummaryView.site_name) \
        .all()

    json_list = list()
    for row in sql_result:
        if len(row) == 1:
            json_list.append(row[0])

    return jsonify(site_names=json_list)


def create_location_dict(category, label, location_sql_result):
    location_list = list(filter(lambda item: item[0], location_sql_result))
    location_list = [x[0] for x in location_list]
    location_dict = {}
    location_dict['locationCategory'] = category
    location_dict['locationLabel'] = label
    location_dict['locationNames'] = location_list
    return location_dict
 
@main.route('/locations')
def all_locations_list():
    result_list = list()

    # Get site names
    site_name_sql_result = CoaSummaryView.query \
        .filter() \
        .with_entities(CoaSummaryView.site_name) \
        .group_by(CoaSummaryView.site_name) \
        .order_by(CoaSummaryView.site_name) \
        .all()
    result_list.append(create_location_dict('site','Site',site_name_sql_result))

    # Get towns
    town_sql_result = CoaSummaryView.query \
        .filter() \
        .with_entities(CoaSummaryView.town) \
        .group_by(CoaSummaryView.town) \
        .order_by(CoaSummaryView.town) \
        .all()
    result_list.append(create_location_dict('town','Town',town_sql_result))

    # Get counties
    county_sql_result = CoaSummaryView.query \
        .filter() \
        .with_entities(CoaSummaryView.county) \
        .group_by(CoaSummaryView.county) \
        .order_by(CoaSummaryView.county) \
        .all()
    result_list.append(create_location_dict('county','County',county_sql_result))

    return jsonify(locations=result_list)


def parse_date_string(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

@main.route('/dirtydozen')
def dirty_dozens():
    # set the values allowed for the location category
    location_category = request.args.get('locationCategory', default = 'site', type = str)
    location_name = request.args.get('locationName', default = 'Union Beach', type = str)
    start_date_str = request.args.get('startDate', default = '2016-1-1', type = str)
    end_date_str = request.args.get('endDate', default = '2018-12-31', type = str)
    
    # convert date strings to dates
    start_date = parse_date_string(start_date_str)
    end_date = parse_date_string(end_date_str)

    result = CoaSummaryView.query \
        .filter(
            CoaSummaryView.site_name == location_name,
            CoaSummaryView.volunteer_date >= start_date,
            CoaSummaryView.volunteer_date <= end_date) \
        .with_entities(
            CoaSummaryView.item_name,
            CoaSummaryView.item_id,
            CoaSummaryView.category,
            CoaSummaryView.material,
            db.func.sum(CoaSummaryView.quantity).label("quantity_sum")) \
        .group_by(CoaSummaryView.item_name) \
        .order_by("quantity_sum desc") \
        .limit(12)

    total_items = CoaSummaryView.query \
        .filter(
            CoaSummaryView.site_name == location_name,
            CoaSummaryView.volunteer_date >= start_date,
            CoaSummaryView.volunteer_date <= end_date) \
        .with_entities(db.func.sum(CoaSummaryView.quantity)) \
        .scalar()

    json_list = []
    for row in result:
        json_list.append(dict(
            itemName=row[0], 
            itemId=row[1],
            categoryName=row[2],
            materialName=row[3],
            count=row[4], 
            percentage=(0 if total_items == None else (row[4] / total_items) * 100)
        ))

    return jsonify(dirtydozen=json_list)

@main.route('/validdaterange')
def valid_date_range():
    #set the arguments for the validdaterange request
    location_category = request.args.get('locationCategory', default = 'site', type = str)
    location_name = request.args.get('locationName', default = 'Union Beach', type = str)
    
    location_category_column = get_location_category_column(location_category)

    db_result = CoaSummaryView.query \
                    .filter(location_category_column == location_name) \
                    .with_entities( \
                        db.func.min(CoaSummaryView.volunteer_date), \
                        db.func.max(CoaSummaryView.volunteer_date)) \
                    .all()
    
    # db_result should have only one value
    result_dict = dict()
    for first_date, last_date in db_result:
        result_dict["firstDate"] = first_date.strftime('%Y-%m-%d')
        result_dict["lastDate"] = last_date.strftime('%Y-%m-%d')
    return jsonify(validDateRange=result_dict)