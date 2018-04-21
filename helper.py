import json
from datetime import datetime
import re
import datetime as dt

master_dict = {}
rooms = {}
room_set = set()

days_of_week = {
    'monday':0,
    'tuesday':1,
    'wednesday':2,
    'thursday':3,
    'friday':4,
    'saturday':5,
    'sunday':6
    }

with open('201820.json','r') as file:
    master_dict = json.loads(file.read())


for subj in master_dict:
    for section in master_dict[subj]['data']:
        subj = section['subjectCourse']
        if len(section['meetingsFaculty']) == 0: continue

        meeting_times = section['meetingsFaculty'][0]['meetingTime']
        start_date = meeting_times['startDate']
        end_date = meeting_times['endDate']

        for key,vals in meeting_times.items():

            build = meeting_times['building']
            room = meeting_times['room']
            if vals == True and key != 'creditHourSession':
                
                start_time = meeting_times['beginTime']
                end_time = meeting_times['endTime']

                if None in [start_time,start_date,end_date,end_time]: continue

                start = datetime.strptime(start_date+start_time, "%m/%d/%Y%H%M")
                second = datetime.strptime(start_date+end_time, "%m/%d/%Y%H%M")
                end = datetime.strptime(end_date, "%m/%d/%Y")

                while start <= end:
                    start += dt.timedelta(days=1)
                    second += dt.timedelta(days=1)

                    if(start.weekday() == days_of_week[key]):
                        room_code = str(build)+str(room)
                        event = {
                         'title': subj,
                         'start': start.__format__("%Y-%m-%dT%H:%M:00"),
                         'end': second.__format__("%Y-%m-%dT%H:%M:00")
                         }

                        room_list = rooms.get(room_code,[])
                        room_list.append(json.dumps(event))
                        rooms[room_code] = room_list
                        room_set.add(room_code)
                        #print(room_code,event)

room_list = list(room_set)
build_dict = {}
for room_ in room_list:
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    match = r.match(room_)
    if match is not None:
        build_set = build_dict.get(match.group(1),set())
        build_set.add(match.group(0))
        build_dict[match.group(1)] = build_set

for key in build_dict:
    build_dict[key] = list(build_dict[key])

room_list = list(room_set)
for room_ in room_list:
    out = []
    for room,classes in rooms.items():
        if room_ == room:
            for class_ in classes:
                day_dict = json.loads(class_)
                out.append(day_dict)
    with open(f'C:\\Users\\etmac\\OneDrive\\Desktop\\Programming\\Full Calendar\\rooms\\{room_}.json','w') as file:
        file.write( 'var class_ = ' +json.dumps(out,indent=4) + ';')