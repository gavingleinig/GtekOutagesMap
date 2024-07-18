import xml.etree.ElementTree as ET
import csv


#this program converts KML to a CSV with 'name', 'x coordinate', 'y coordinate', 'description' 
#Note that the description contains other text in addition to the tower radius, so it needs to be manually cleaned before initializing  the database

namespaces = {
    'kml': 'http://www.opengis.net/kml/2.2',
}

tree = ET.parse('doc.kml')
root = tree.getroot()


with open('towersLocationsRange.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(['name', 'x coordinate', 'y coordinate', 'description'])

    for placemark in root.findall('.//kml:Placemark', namespaces):
        name = placemark.find('kml:name', namespaces).text
        description_lines = placemark.find('kml:description', namespaces).text.strip().split('\n')
        description_lines = [line for line in description_lines if 'mile' in line]
        description = description_lines[0] if description_lines else ''
        #description = [line.split(' ')[0] for line in description_lines if 'mile max range' in description]#FIXME!!!
        coordinates = placemark.find('.//kml:coordinates', namespaces).text.strip()
        x_coordinate, y_coordinate, _ = coordinates.split(',')

        csvwriter.writerow([name, x_coordinate, y_coordinate, description])
