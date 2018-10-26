from flask import render_template, request, jsonify
from . import main
from ..models import Item, CoaSummaryView
import datetime
from .. import db

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

@main.route('/getsitesdropdownlist')
def site_list():
    sql_result = CoaSummaryView.query.filter().\
                                      with_entities(CoaSummaryView.site_name).\
                                      group_by(CoaSummaryView.site_name).\
                                      order_by(CoaSummaryView.site_name).\
                                      all()
    json_list = list()
    for row in sql_result:
        if len(row) == 1:
            print(row)
            json_list.append(row[0])

    return jsonify(site_names=json_list)

@main.route('/locations')
def all_locations_list():
    result_list = list()
    #Get site names
    site_name_sql_result = CoaSummaryView.query.filter().\
                                      with_entities(CoaSummaryView.site_name).\
                                      group_by(CoaSummaryView.site_name).\
                                      order_by(CoaSummaryView.site_name).\
                                      all()
    #Remove Nulls
    site_name_list = list(filter(lambda item: item[0], site_name_sql_result))
    site_name_list = [x[0] for x in site_name_list]
    site_name_dict = {}
    site_name_dict['locationCategory'] = 'site'
    site_name_dict['locationLabel'] = 'Site'
    site_name_dict['locationNames'] = site_name_list
    result_list.append(site_name_dict)

    #Get towns
    town_sql_result = CoaSummaryView.query.filter().\
                                      with_entities(CoaSummaryView.town).\
                                      group_by(CoaSummaryView.town).\
                                      order_by(CoaSummaryView.town).\
                                      all()
    town_list = list(filter(lambda item: item[0], town_sql_result))
    town_list = [x[0] for x in town_list]
    town_dict = {}
    town_dict['locationCategory'] = 'town'
    town_dict['locationLabel'] = 'Town'
    town_dict['locationNames'] = town_list
    result_list.append(town_dict)

    #Get counties
    county_sql_result = CoaSummaryView.query.filter().\
                                      with_entities(CoaSummaryView.county).\
                                      group_by(CoaSummaryView.county).\
                                      order_by(CoaSummaryView.county).\
                                      all()
    county_list = list(filter(lambda item: item[0], county_sql_result))
    county_list = [x[0] for x in county_list]
    county_dict = {}
    county_dict['locationCategory'] = 'county'
    county_dict['locationLabel'] = 'County'
    county_dict['locationNames'] = county_list
    result_list.append(county_dict)

    return jsonify(locations=result_list)


@main.route('/dirtydozen')
def dirty_dozens():
    #set the values allowed for the location category
    location_category = request.args.get('locationCategory', 
                                          default = 'site', type = str)
    #site_id = request.args.get('siteId',default = 0, type = int)
    location_name = request.args.get('locationName',
                                 default = 'Union Beach', type = str)

    start_date_str = request.args.get('startDate',
                                    default = '2016-1-1', type = str)

    end_date_str = request.args.get('endDate',
                                default = '2018-12-31', type = str)
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    result = CoaSummaryView.query.filter(CoaSummaryView.site_name == location_name, \
                                           CoaSummaryView.volunteer_date > start_date,
                                           CoaSummaryView.volunteer_date < end_date). \
                                           with_entities(CoaSummaryView.item_name, \
                                           db.func.sum(CoaSummaryView.quantity)). \
                                           group_by(CoaSummaryView.item_name)

    #remove the NULL item_name
    result = filter(lambda item: item[0], result)
    result = sorted(result, key=lambda tup:tup[1], reverse = True)
    result = result[:12]
    result_dict = dict((x,y) for x,y in result)
    return jsonify(items=result_dict)

