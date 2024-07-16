import xml.etree.ElementTree as ET
import csv

# Define the namespaces
namespaces = {
    'kml': 'http://www.opengis.net/kml/2.2',
    'gx': 'http://www.google.com/kml/ext/2.2',
    'atom': 'http://www.w3.org/2005/Atom'
}

# Parse the XML file
tree = ET.parse('doc.kml')
root = tree.getroot()

# Prepare the CSV file
with open('towersLocationsRange.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['name', 'x coordinate', 'y coordinate', 'description'])

    # Iterate over each Placemark in the XML
    for placemark in root.findall('.//kml:Placemark', namespaces):
        name = placemark.find('kml:name', namespaces).text
        description_lines = placemark.find('kml:description', namespaces).text.strip().split('\n')
        description_lines = [line for line in description_lines if 'mile' in line]
        description = description_lines[0] if description_lines else ''
        description = [line.split(' ')[0] for line in description_lines if 'mile max range' in description]#FIXME!!!
        coordinates = placemark.find('.//kml:coordinates', namespaces).text.strip()
        x_coordinate, y_coordinate, _ = coordinates.split(',')

        # Write the row to the CSV
        csvwriter.writerow([name, x_coordinate, y_coordinate, description])
