from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
import requests
import json
import folium
import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

ACAD_YEAR = "2018-2019"
SEM = "1"
URL = "http://api.nusmods.com/{}/{}/timetable.json".format(ACAD_YEAR, SEM)
MODSdata = requests.get(URL)
timetable = MODSdata.json();

venue_data_computing = {
'Com1' :[ "COM1-0217", "COM1-0216", "COM1-B110", "COM1-0212", "COM1-VCRM", "COM1-0114", "COM1-0204", "COM1-0113", "COM1-0207", "COM1-0120", "COM1-0209", "COM1-B111", "COM1-B112", "COM1-B108", "COM1-B109", "COM1-0218", "COM1-0203", "COM1-0208", "COM1-0201", "COM1-0210", "COM1-B103", "COM1-0206", "COM1-B113", "COM1-B102" ],
'Com2' :[ "COM2-0108", "LT16", "LT17", "LT18", "LT19", "SR_LT19" ],
'I3' :[ "I3-0338", "I3-0339", "I3-0344", "I3-AUD", "I3-0336", "I3-0337" ]
}

venue_data_arts = {
'As1' : [ "AS1-0207", "AS1-0205", "AS1-0304", "AS1-0301", "AS1-0303", "AS1-0201", "AS1-0203", "AS1-0302", "AS1-0204", "AS1-0213", "AS1-0209", "AS1-0208", "AS1-0211", "AS1-0210", "AS1-0524", "AS1-0212", "LT10", "LT9" ],
'As2' : [ "AS2-0413", "AS2-0311", "AS2-0510", "AS2-0509", "AS2-0312", "AS2-ELAB", "AS2-0203", "AS2-0204", "AS2-0313", "AS2-0302", "AS2-0316", "AS2-0201", "LT12", "LT11", "LT13" ],
'As3' : [ "AS3-0215", "AS3-0304", "AS3-0302", "AS3-0303", "AS3-0214", "AS3-0208", "AS3-0209", "AS3-0308", "AS3-0309", "AS3-0307", "AS3-0305", "AS3-0306", "AS3-0212", "AS3-0213", "AS3-0312", "AS3-0314", "AS3-0316", "AS3-0523", "AS3-0101" ],
'As4' : [ "AS4-0603", "AS4-0604", "AS4-0206", "AS4-0116", "AS4-0118", "AS4-0335", "AS4-0601", "AS4-0602", "AS4-0117", "AS4-0119", "AS4-0109", "AS4-B110", "AS4-0114", "AS4-0318", "AS4-B107", "AS4-0208", "AS4-0115", "AS4-B109" ],
'As5' : [ "AS5-0202", "AS5-0309", "AS5-0203", "AS5-0204", "AS5-0205", "LT8" ],
'As6' : [ "AS6-0214", "AS6-0212", "AS6-0421", "AS6-0426", "AS6-0208", "AS6-0333", "AS6-0215B", "AS6-0338", "LT14", "LT15" ],
'As7' : [ "AS7-0101", "AS7-0102", "AS7-0119", "AS7-0106", "AS7-0214", "AS7-0201A", "AS7-0201" ],
'As8' : [ "AS8-0646", "AS8-0402", "AS8-0401", "AS8-0405", "AS8-0647" ]
}

venue_data_science = {
'S1' : [ "S1A-0217", "S1A-04LAB3", "S1A-03LAB1", "S1A-03LAB6", "S1A-03LAB2", "S1A-04LAB4", "LT32" ],
'S2' : [ "S2-0414", "S2-04LAB5", "S2-0415", "S2-03LAB7" ],
'S3' : [ "LT20" ],
'S4' : [ "S4-02LAB", "S4-04LAB", "LT21" ],
'S5' : [ "S5-01PHYS", "S5-0410", "S5-01GEN", "S5-0224", "S5-0223" ],
'S6' : [ "S6-04" ],
'S7' : [ "S7-0401" ],
'S8' : [ "S8-0314", "S8-0403" ],
'S11' : [ "S11-0301", "S11-0204", "S11-0302A", "S11-0302", "S11-0401A" ],
'S12' : [ "S12-0402", "S12-0401", "S12-0402A", "S12-0402B", "S12-0402C", "S12-0402D", "S12-0403" ],
'S13' : [ "S13-M-08", "S13-M-09", "S13-0313" ],
'S14' : [ "S14-0619", "S14-0503", "S14-0620" ],
'S16' : [ "S16-0430", "S16-0436", "S16-0307", "S16-0431", "S16-0598", "S16-0440", "S16-0306", "S16-0435", "S16-0309", "S16-0304", "S16-0437", "S16-06118", "S16-05101", "S16-05102", "LT31", "LT26" ],
'S17' : [ "S17-0404", "S17-0406", "S17-0302", "S17-0405", "S17-0611", "S17-0304", "S17-0512", "S17-0511", "LT34", "LT33" ],
'Lt27' : [ "LT27", "LT28", "LT29" ]
}

venue_data_business = {
'Biz1' : [ "BIZ1-0206", "BIZ1-0301", "BIZ1-0303", "BIZ1-0201", "BIZ1-0202", "BIZ1-0205", "BIZ1-0305", "BIZ1-0203", "BIZ1-0304", "BIZ1-0204", "BIZ1-SR6-1", "BIZ1-0302", "BIZ1-CMRI", "BIZ1-0307" ],
'Biz2' : [ "BIZ2-0117", "BIZ2-0404", "BIZ2-0118", "BIZ2-0301", "BIZ2-0226", "BIZ2-0224", "BIZ2-0201", "BIZ2-B104", "BIZ2-0510", "BIZ2-0413B", "BIZ2-0202", "BIZ2-0413C", "BIZ2-0413A", "BIZ2-0112", "BIZ2-0228", "BIZ2-0302", "BIZ2-0229", "BIZ2-0420", "BIZ2-0303", "BIZ2-0227", "BIZ2-0509", "BIZ2-0116", "BIZ2-0115", "BIZ2-0401B" ]
}

venue_data_engineering = {
'E1' : [ "E1-06-08", "E1-06-07", "E1-06-05", "E1-06-01", "E1-06-09", "E1-06-04", "E1-06-02", "E1-06-06", "E1-06-03", "E1-06-10", "E1-06-13", "E1-06-11", "E1-06-16", "E1-06-14", "E1-06-12", "E1-06-15", "E1A-05-19", "E1-0410PC2", "LT5" ],
'E2' : [ "E2-03-02", "E2-03-08", "E2-03-09", "E2-03-06", "E2A-02-02", "E2A-03-01", "E2A-02-01", "E2-03-03", "E2-03-32", "LT2", "LT1" ],
'E3' : [ "E3-06-01", "E3-06-02", "E3-06-05", "E3-06-06", "E3-06-04", "E3-06-15", "E3-06-09", "E3-06-03", "E3-0605-06", "E3-06-11", "E3-06-12", "E3-06-13", "E3-06-08", "E3-06-10", "E3-06-07", "E3-06-14", "E3-05-21", "E3-03-01", "E3A-05-07", "E3A-05-03" ],
'E4' : [ "E4-04-04", "E4-04-02", "E4-04-03", "E4A-04-08", "E4-03-07", "E4A-06-03", "E4A-06-07", "E4-07-09", "LT6" ],
'E5' : [ "E5-03-20", "E5-02-32", "E5-03-22", "E5-03-23", "E5-03-21", "E5-03-24", "E5-03-19", "LT3", "LT4" ],
'E6' : [],
'Ea' : [ "EA-02-11", "EA-06-03", "EA-06-06", "EA-06-07", "EA-06-05", "EA-06-02", "EA-06-04", "LT7A", "LT7" ],
'Ew1' : [ "EW1-1M-02", "EW1-1M-03", "EW2-04-02", "EW2-03-14" ],
'Ew2' : []
}

venue_data_design = {
'SDE' : [ "SDE-427", "SDE-423", "SDE-426", "SDE-422", "SDE-SR9", "SDE-SR15", "SDE-421", "SDE-SR10", "SDE-SR11", "SDE-SR14", "SDE-425", "SDE-SR13", "SDE-424", "SDE-ER4", "SDE-SR12", "SDE-ER1", "SDE_ER4-5", "SDE-ES2", "SDE-ER5", "SDE-ISD-1", "SDE-ISD-2", "SDE-ES1" ],
'CELC' : [ "CELC-SR1A", "CELC-TR7", "CELC-SR1B", "CELC-TR6" ]
}

venue_data_utown = {
'UT' : [ "UT-AUD3", "UTSRC-LT50", "UTSRC-LT51", "UT-AUD2", "UTSRC-LT53", "UT-AUD1", "UTSRC-GLR", "UTSRC-LT52", "UTSRC-SR8", "UTSRC-SR9", "UTSRC-SR7", "UTSRC-SR4", "UTSRC-SR6", "UTSRC-SR2", "UTSRC-SR3", "UTSRC-SR5", "UTSRC-SR1", "UTSRC-PR1" ],
'ERC' : [ "ERC-SR11", "ERC-GLR", "ERC-SR3", "ERC-ALR", "ERC-SR10", "ERC-SR4", "ERC-SR5", "ERC-SR8", "ERC-SR9CAM" ],
'USP' : [ "USP-MML", "USP-SR1", "USP-TR1", "USP-SR3", "USP-SR2", "USP-MC" ],
'CAPT' : [ "CAPT-SR3", "CAPT-SR1-2", "CAPT-SR4", "CAPT-SR6", "CAPT-SR5" ],
'RC4' : [ "RC4-SR3", "RC4-SR1-2", "RC4-SR5", "RC4-SR6", "RC4-SR4", "RC4-SR1", "RC2-G-02" ],
'TC' : [ "TC-SR4", "TC-SR5", "TC-SR3", "TC-TR2", "TC-SR6" ]
}

venue_data_rvrc = {
'RVRC' : [ "RVR-SRM01", "RVR-SRM04", "RVR-SRM02", "RVR-ATRM", "RVR-SRM03", "RVR_MPR1", "RVR_MPR2", "RVR-MPR02", "RVR-MPR01" ]
}
venue_data_yale = {
'Yale' :[ "Y-PgRm2", "Y-CR1", "Y-PerfHall", "Y-CR4", "Y-CR5", "Y-CR6", "Y-CR7", "Y-CR8", "Y-CR2", "Y-CR3", "Y-GLRm1", "Y-GLRm2", "Y-KChanrai", "Y-CR15", "Y-CR17", "Y-CR18", "Y-CR9", "Y-CR13", "Y-CR14", "Y-CR19", "Y-CR20", "Y-CR21", "Y-CR12", "Y-CR22", "Y-ArtsStud", "Y-PracRm6", "Y-CR11", "Y-PgRm1", "Y-CR23", "Y-AChemLab", "Y-PhysLab", "Y-LT1", "Y-CR16", "Y-CompLab" ]
}

venue_data_med = {
'Md1' :[ "MD1-07-01A", "MD1-05-01A", "MD1-06-01A", "MD1-06-03M", "MD1-03-01C", "MD1-03-01B", "MD1-08-01E", "MD1-09-01A", "MD1-0903EF", "MD1-08-03E", "MD1-08-01B", "MD1-09-03F", "MD1-0801AB" ],
'Md4' :[ "MD4-02-03E", "MD4_LAB9" ],
'Md7' :[ "MD7_LAB8", "MD7-02-03" ],
'Md10' :[ "MD10-01-01" ],
'Md11' :[ "MD11-01-03", "MD11CRCAUD" ],
'CELS' :[ "CELS-01-08", "CELS-04-01" ]
}

venue_data_music = {
'YSTCM' : [ "YSTCM-SR7", "YSTCM-RS", "YSTCM-SR3", "YSTCM-WS", "YSTCM-TR", "YSTCM-SR4", "YSTCM-SR2", "YSTCM-SR6", "YSTCM-SR8", "YSTCM-ER3", "YSTCM-HALL", "YSTCM-SR1", "YSTCM-RECS", "YSTCM-ER2", "YSTCM-ER4", "YSTCM-OH", "YSTCM-ER6", "YSTCM-SR5", "YSTCM-MLAB" ]
}

faculties = {
'Com' : venue_data_computing,
'Arts' : venue_data_arts,
'Sci' : venue_data_science,
'Biz' : venue_data_business,
'Eng' : venue_data_engineering,
'Dsgn' : venue_data_design,
'Utwn' : venue_data_utown,
'RVRC' : venue_data_rvrc,
'Yale' : venue_data_yale,
'Med' : venue_data_med,
'Music' : venue_data_music
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
    days = SelectField('days', choices = [(" "," "), ("Monday","Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")])

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
    venues_final = []
    day = ''

    #get results to show, database entry w buildings, when search button is pressed -> all venues in that faculty is searched, sort result by building
    if request.method == 'POST':

        if form.days.data == ' ':
            day = datetime.date.today().strftime("%A")
        else:
            day = form.days.data


        if str(form.faculty.data) in faculties:
            venue_data = faculties[str(form.faculty.data)]

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
                            names.append((name , slot.get("Venue")))
                    #names.append(name)

        #return render_template('results.html', venues=names)
        end_time = 0
        for mod in timetable:
            for slot in mod.get("Timetable", ()):
                venue == slot.get("Venue")
                for x in range(len(venues)-1):

                    if (venue == venues[x][1]):
                        end_time = 5
                        venues_final.append((venues[x],venue))


        #return render_template('results.html', venues=names)
        return render_template('results.html', venues=venues)
        #return results[1] + ''
                #return jsonify({'time' :timetable}) #testing if can access url
        #return '<h1>Faculty: {}, Building: {}, Time requested: {}</h1>'.format(form.faculty.data, building.name, form.time.data)


    return render_template('index.html', form=form, day = day)

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

location_data = {
'Com1' : [1.295164, 103.773871],
'Com2' : [1.294334, 103.774111],
'I3' : [1.292920, 103.775389],
'As1' : [1.295194, 103.772167],
'As2' : [1.295242, 103.771109],
'As3' : [1.294778, 103.771068],
'As4' : [1.294569, 103.771760],
'As5' : [1.294364, 103.771873],
'As6' : [1.295799, 103.773279],
'As7' : [1.294545, 103.770902],
'As8' : [1.296700, 103.772356],
'SDE' : [1.297506, 103.770516],
'CELC' : [1.297271, 103.771386],
'Biz1' : [1.292465, 103.774048],
'Biz2' : [1.293463, 103.775133],
'S1' : [1.295557, 103.777962],
'S2' : [1.295545, 103.778276],
'S3' : [1.295550, 103.778619],
'S4' : [1.295619, 103.779161],
'S5' : [1.295517, 103.779759],
'S6' : [1.295083, 103.780403],
'S7' : [ 1.296351, 103.778971],
'S8' : [1.296271, 103.779320],
'S11':[1.296797, 103.778822],
'S12':[1.296997, 103.778736],
'S13':[1.296800, 103.779254],
'S14':[1.297006, 103.779897],
'S16':[1.296952, 103.780256],
'S17':[1.297787, 103.780479],
'LT27':[1.297452, 103.780834],
'E1':[1.298726, 103.771206],
'E2':[1.299603, 103.771164],
'E3':[1.299779, 103.771707],
'E4':[1.298844, 103.771957],
'E5':[1.298346, 103.772032],
'E6' : [1.1296271, 103.779320],
'Ea':[1.300432, 103.770768],
'Ew1':[1.299198, 103.770564],
'Ew2':[1.299359, 103.772517],
'Md1':[1.295593, 103.780505],
'Md4':[1.295878, 103.780873],
'Md7':[1.296521, 103.781087],
'Md10':[1.297122, 103.781946],
'Md11':[1.297379, 103.781903],
'CELS':[1.295449, 103.780272],
'YSTCM':[1.302473, 103.773010],
'UT' : [1.304867, 103.772193],
'ERC' : [1.305677, 103.772736],
'USP' : [1.306843, 103.773041],
'CAPT' : [1.307784, 103.773192],
'RC4' : [1.308149, 103.773309],
'TC' : [1.306210, 103.773729]
}

@app.route('/map/<string:building>')

def map(building):
    if building in location_data:

        return render_template('map.html', x =location_data[building][0], y =location_data[building][1])
    return 'no map'


if __name__ == '__main__':
    app.run(debug=True)
