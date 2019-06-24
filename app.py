from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

ACAD_YEAR = "2018-2019"
SEM = "1"
URL = "http://api.nusmods.com/{}/{}/timetable.json".format(ACAD_YEAR, SEM)
day = "Monday" #adjust clock here
MODSdata = requests.get(URL)
timetable = MODSdata.json();

venue_data = {
'Com1' :[ "COM1-0217", "COM1-0216", "COM1-B110", "COM1-0212", "COM1-VCRM", "COM1-0114", "COM1-0204", "COM1-0113", "COM1-0207", "COM1-0120", "COM1-0209", "COM1-B111", "COM1-B112", "COM1-B108", "COM1-B109", "COM1-0218", "COM1-0203", "COM1-0208", "COM1-0201", "COM1-0210", "COM1-B103", "COM1-0206", "COM1-B113", "COM1-B102" ],
'Com2' :[ "COM2-0108", "LT16", "LT17", "LT18", "LT19", "SR_LT19" ],
'I3' :[ "I3-0338", "I3-0339", "I3-0344", "I3-AUD", "I3-0336", "I3-0337" ]
}

def get_time():
    time = []
    for i in range(6,24):
        time.append(('{i:02d}00'.format(i=i),'{i:02d}00'.format(i=i)))
        time.append(('{i:02d}30'.format(i=i),'{i:02d}30'.format(i=i)))
    return time

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(50))
    name = db.Column(db.String(50))

class Form(FlaskForm):
    faculty = SelectField('faculty', choices=[('Com', 'Computing'), ('Arts', 'Arts'),
    ('Sci','Science'),('Biz', 'Business'),('Eng', 'Engineering'),('Dsgn', 'Design'),
    ('Utwn', "Utown"), ('RVRC', "RVRC"), ('Yale', 'Yale'), ('Med', "Medicine"), ('Music', "Music")])
    building = SelectField('building', choices=[])
    time = SelectField('time', choices = get_time())

class Slot():
	def __init__(self, code, name, slot):
		self.code = code
		self.name = name
		self.lesson_type = slot.get("LessonType")
		self.class_num = slot.get("ClassNo")
		self.venue = slot.get("Venue")
		self.start_time = slot.get("StartTime")
		self.end_time = slot.get("EndTime")
		self.day = slot.get("DayText")
		self.week = slot.get("WeekText")

        def str():
            return self.venue + ''


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    form.building.choices = [(building.id, building.name) for building in Building.query.filter_by(faculty='Com').all()]

    venues = []
    names = []

    #get results to show, database entry w buildings, when search button is pressed -> all venues in that faculty is searched, sort result by building
    if request.method == 'POST':

        if form.faculty.data == "Com":
            for buildings in venue_data:
                building_name = buildings
                building_size = len(venue_data[str(building_name)])
                for x in range(building_size):
                    venues.append((building_name,venue_data[str(building_name)][x]))

        #return render_template('results.html', venues=venues)

        building = Building.query.filter_by(id=form.building.data).first()
        #take all venues from database
        for mod in timetable:
            name = mod.get("ModuleCode")
            for slot in mod.get("Timetable", ()):
                venue = slot.get("Venue")
                if ((slot.get("StartTime") <= form.time.data <= slot.get("EndTime"))
                and (slot.get("DayText") == day)):
                    for x in range(len(venues)-1):
                        if venues[x][1] == slot.get("Venue"):
                            del venues[x] #tuple
                            names.append(name + ' ' + slot.get("Venue"))
                    #names.append(name)

        #return render_template('results.html', venues=names)
        return render_template('results.html', venues=venues)
        #return results[1] + ''
                #return jsonify({'time' :timetable}) #testing if can access url
        #return '<h1>Faculty: {}, Building: {}, Time requested: {}</h1>'.format(form.faculty.data, building.name, form.time.data)


    return render_template('index.html', form=form)

@app.route('/building/<faculty>')
def building(faculty):
    cities = Building.query.filter_by(faculty=faculty).all()

    buildingArray = []

    for building in cities:
        buildingObj = {}
        buildingObj['id'] = building.id
        buildingObj['name'] = building.name
        buildingArray.append(buildingObj)

    return jsonify({'cities' : buildingArray})

if __name__ == '__main__':
    app.run(debug=True)
