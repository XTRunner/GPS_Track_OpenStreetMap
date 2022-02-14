import requests
import xml.etree.ElementTree as ET
import os


def retrieve_xml_by_bounding_box(min_x, max_x, min_y, max_y, page_num=0):
    # OSM API v0.6: Get /api/0.6/trackpoints?bbox=left,bottom,right,top&page=pageNumber
    # Reference: https://wiki.openstreetmap.org/wiki/API_v0.6#GPS_traces
    # Example: https://api.openstreetmap.org/api/0.6/trackpoints?bbox=0,51.5,0.25,51.75&page=0

    url_api = 'https://api.openstreetmap.org/api/0.6/trackpoints'

    xml = requests.get(url_api, params={'bbox': ','.join([str(min_x), str(min_y), str(max_x), str(max_y)]),
                                        'page': page_num}).text

    return xml


def parse_xml(xml_text, track_counter):
    root = ET.fromstring(xml_text)

    file_name = track_counter

    #print('root', root.tag, root.attrib)
    #for child in root:
    #    print(child.tag, child.attrib)

    # '.tag' of each track/trajectory is 'trk'
    selector_track = './/{http://www.topografix.com/GPX/1/0}trk'

    for trk in root.findall(selector_track):
        # '.tag' of each data point in each track/trajectory is 'trkpt'
        selector_lat_lon = './/{http://www.topografix.com/GPX/1/0}trkpt'

        with open('tracks_OSM/' + str(file_name) + '.txt', 'a') as f:
            for trkpt in trk.findall(selector_lat_lon):
                lat, lon = trkpt.attrib['lat'], trkpt.attrib['lon']
                f.writelines([lat, lon])
                f.writelines('\n')

        f.close()

        file_name += 1

    return file_name, file_name - track_counter


def main():
    if not os.path.exists('tracks_OSM'):
        os.mkdir('tracks_OSM')

    # Interest of Area to retrieve the track
    ### MODIFY BASED ON THE REQUEST
    left, right, bottom, top = -74.25, -73.75, 40.650, 41.15
    # Merely for naming different tracks
    track_counter = 0

    cur_x = left

    while cur_x < right:
        cur_y = bottom

        while cur_y < top:
            cur_page = 0
            track_count_per_area = 0

            print("Now dealing with area ", cur_x, min(cur_x + 0.25, right), cur_y, min(cur_y + 0.25, top))

            while True:
                # Note that the max bbox range is 0.25
                xml = retrieve_xml_by_bounding_box(cur_x, min(cur_x+0.25, right), cur_y, min(cur_y+0.25, top),
                                                   page_num=cur_page)

                track_counter, increase_track_num = parse_xml(xml, track_counter)

                track_count_per_area += increase_track_num

                if increase_track_num == 0:  # current page has no valid path
                    print("No more track in the current area --", track_count_per_area, " tracks")
                    break

                if track_count_per_area > 1000:  # Enough track from the current sub-bounding-box
                    print("Retrieve enough tracks in the current area -- ", track_count_per_area, " tracks")
                    break

                cur_page += 1

                print("Retrieved in total ", track_counter, " track")

            cur_y += 0.25

        cur_x += 0.25


if __name__ == '__main__':
    main()
