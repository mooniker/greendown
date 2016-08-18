import requests, json

colorCode = 'GR'
demo_key = '6b700f7ea9db408e9745c207da7ca827'

url = 'https://api.wmata.com/Rail.svc/json/jStations?' + colorCode + '&api_key=' + demo_key
print url
req = requests.get(url)

# print(req.json()['Stations'])
stations = req.json()['Stations']

def getStationByColor(station):
    if station['LineCode1'] == colorCode or station['LineCode2'] == colorCode or station['LineCode3'] == colorCode or station['LineCode4'] == colorCode:
        return True
    return False

def getStationCode(station):
    return station['Code']

green_stations = filter(getStationByColor, stations)
# print map(lambda s: s['Name'] + str(s['Lat']) + str(s['Lon']), green_stations)
green_station_codes = map(getStationCode, green_stations)
#
# print(green_station_codes)

# green_stations_codes = ['E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11']

def is_target_colored_station(station):
    return station['StationCode'] in green_station_codes

elevators_url = 'https://api.wmata.com/Incidents.svc/json/ElevatorIncidents?api_key=' + demo_key
req_elevators = requests.get(elevators_url).json()['ElevatorIncidents']
green_station_elevator_issues = filter(is_target_colored_station, req_elevators)
green_station_elevator_issues = filter(lambda s: s['UnitType'] == 'ELEVATOR', green_station_elevator_issues)
# print green_station_elevator_issues

for station in green_stations:
    station_string = station['Name'] + ' (' + str(station['Lat']) + ', ' + str(station['Lon']) + ')'
    if station['Name'] in map(lambda s: s['StationName'], green_station_elevator_issues):
        print station_string + ' ELEVATOR BROKEN :('
    else:
        print station_string
