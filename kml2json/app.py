import json
import xml.etree.ElementTree as ET

NS = {'kml': 'http://www.opengis.net/kml/2.2'}
ROOT = ET.parse('import.kml').getroot()


class Helper(object):
    def __init__(self):
        pass

    # @staticmethod
    def getType(placemark):
        ExtendedData = placemark.find('kml:ExtendedData', NS)
        ExtendedData_Data = ExtendedData.find('kml:Data', NS)
        ExtendedData_Data_value_type = ExtendedData_Data.find('kml:value', NS)

        return ExtendedData_Data_value_type.text


class MyDict(dict):
    def __str__(self):
        return json.dumps(self)


class Section(Helper):
    def __init__(self, title):
        self.title = title
        self.className = 'poi'
        self.keys = list()

    def getAsDictonary(self):
        return {'title': self.title,
                'className': self.className,
                'keys': self.keys}


class Key(dict):
    def __init__(self, coordinates, text, type):
        self.coordinates = coordinates  # [19.67921, -72.14910, 17]
        self.text = text
        self.type = type

    def getAsDictonary(self):
        return {'coordinates': self.coordinates,
                'text': self.text,
                'type': self.type}


class Map(Helper):
    def __init__(self, title, description, displayPopup, sections):
        self.title = title
        self.description = description
        self.displayPopup = bool(displayPopup)
        self.sections = list(sections)

    def getAsDictonary(self):
        return {'title': self.title,
                'description': self.description,
                'displayPopup': self.displayPopup,
                'sections': self.sections}


def main():

    t = []
    keys = []
    for placemark in ROOT[0].findall('kml:Placemark', NS):
        type = Helper.getType(placemark)
        # print('Type: ', type)
        t.append(type)

        name = placemark.find('kml:name', NS)
        # print('Name: ', name.text)

        Point = placemark.find('kml:Point', NS)
        Point_coordinates = Point.find('kml:coordinates', NS)
        # print('Coordinates: ', Point_coordinates.text)

        coords = Point_coordinates.text.split(',')
        coord = [coords[1], coords[0], 14]
        keys.append(Key(coord, name.text, type).getAsDictonary())

        del coord

    tu = list(set(t))  # removing duplicates in lists

    sections = []
    for t in tu:
        sections.append(Section(t).getAsDictonary())

    for section in sections:
        for key in keys:
            if section['title'] == key['type']:
                section['keys'].append(key)

    map = Map('CHT Map', '', True, sections)
    print(json.dumps(map.getAsDictonary()))

if __name__ == '__main__':
    main()
