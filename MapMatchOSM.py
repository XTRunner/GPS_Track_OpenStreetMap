# from leuvenmapmatching.map.inmem import InMemMap
# from leuvenmapmatching.matcher.distance import DistanceMatcher
# from leuvenmapmatching import logger
# import logging
# import osmnx as ox
# import pickle
import os
# import sys
import requests
import json

# logger.setLevel(logging.INFO)  # or if you want to see all steps: logging.DEBUG
# logger.addHandler(logging.StreamHandler(sys.stdout))  # add only if you don't see any output, otherwise it appears double

'''
def retrieve_map_from_OSM(min_x, max_x, min_y, max_y):
    print("Start Downloading Road Network of bbox", min_x, max_x, min_y, max_y, " From OpenStreetMap")

    # Reference: https://osmnx.readthedocs.io/en/stable/osmnx.html#module-osmnx.graph
    osm_network = ox.graph_from_bbox(max_y, min_y, max_x, min_x, network_type='drive', truncate_by_edge=True)

    print("Done with OSM Network Download")

    f_name = '_'.join([str(min_x), str(max_x), str(min_y), str(max_y)])
    f_name = f_name.replace('.', '-')

    with open("map_OSM/" + f_name + ".pkl", 'wb') as f:
        pickle.dump(osm_network, f)

    return osm_network


def construct_map_from_xml(osm_graph):
    my_map = InMemMap('MyOSM', use_latlon=True, use_rtree=True, index_edges=True)

    for node_id, node_inf in osm_graph.nodes(data=True):
        my_map.add_node(node_id, (node_inf['y'], node_inf['x']))

    for start_node, end_node, edge_inf in osm_graph.edges(data=True):
        if start_node != end_node:
            my_map.add_edge(start_node, end_node)
            my_map.add_edge(end_node, start_node)
            #if not edge_inf['oneway']:
            #    my_map.add_edge(end_node, start_node)

    my_map.purge()

    return my_map


def map_match_leu(path, my_map):
    my_matcher = DistanceMatcher(my_map, max_dist_init=300, obs_noise=50, obs_noise_ne=50,
                                 non_emitting_states=True, max_lattice_width=5)
    #my_matcher = SimpleMatcher(my_map, max_dist_init=150, obs_noise=50, obs_noise_ne=50)
    status, _ = my_matcher.match(path)

    # mapviz.plot_map(my_map, matcher=my_matcher, show_labels=True, filename= "output.png")

    return my_matcher.path_pred_onlynodes
'''


def map_match_osrm(path):
    # http://router.project-osrm.org/match/v1/{profile}/{coordinates}
    # ?steps={true|false}&geometries={polyline|polyline6|geojson}&overview={simplified|full|false}&annotations={true|false}

    # Reference: http://project-osrm.org/docs/v5.22.0/api/?language=cURL#match-service
    # url_host = 'http://router.project-osrm.org'

    # Start Docker before using localhost
    url_host = 'http://127.0.0.1:5000'
    url_service = 'match'
    url_version = 'v1'
    url_profile = 'drive'

    url_path = ';'.join(["{},{}".format(lat_lon[1], lat_lon[0]) for lat_lon in path])

    url_api = url_host + '/' + url_service + '/' + url_version + '/' + url_profile + '/' + url_path

    xml = requests.get(url_api, params={'overview': 'full'}).text

    return xml


def main():
    """
    if not os.path.exists('map_OSM'):
        os.mkdir('map_OSM')

    left, right, bottom, top = -74.25, -73.75, 40.650, 41.15

    f_name = '_'.join([str(left), str(right), str(bottom), str(top)])
    f_name = f_name.replace('.', '-')

    if not os.path.exists("map_OSM/" + f_name + ".pkl"):
        osm_g = retrieve_map_from_OSM(left, right, bottom, top)
    else:
        with open("map_OSM/" + f_name + ".pkl", 'rb') as f:
            osm_g = pickle.load(f)

        print("Loaded OSM Network from local")

    my_map = construct_map_from_xml(osm_g)

    for root, dirs, files in os.walk('tracks_OSM'):
        for file in files:
            with open(os.path.join(root, file)) as f:
                path = []

                print("Dealing with track ", os.path.join(root, file))
                lines = f.readlines()

                for line in lines:
                    if line.strip():
                        lat, lon = line.split('-')
                        path.append((float(lat), -float(lon)))

            matched_path = map_match_leu(path, my_map)

            if not matched_path:
                continue
    """

    if not os.path.exists('tracks_matched'):
        os.mkdir('tracks_matched')

    for root, dirs, files in os.walk('tracks_OSM'):
        for file in files:
            with open(os.path.join(root, file)) as f:
                path = []

                lines = f.readlines()

                for line in lines:
                    if line.strip():
                        # I forgot to add delimiter in the previous code... My bad
                        lat, lon = line.split(',')
                        path.append((float(lat), float(lon)))

            result = map_match_osrm(path)

            parsed = json.loads(result)

            # magic happens here to make it pretty-printed
            # print(json.dumps(parsed, indent=4, sort_keys=True))
            # matched_path = []

            if 'tracepoints' in parsed:
                with open('tracks_matched/' + file, 'a') as f:
                    for idx, element in enumerate(parsed['tracepoints']):
                        # tracepoints - location - [lon, lat]
                        # matched_path.append((element['location'][1], element['location'][0]))
                        if element is not None:  # Might be None due to nothing found to match
                            f.writelines([str(element['location'][1]), ', ',
                                          str(element['location'][0]), ', ',
                                          str(element['waypoint_index'])])

                            f.writelines('\n')
                        else:
                            f.writelines(["None"])
                            f.writelines('\n')

                    f.close()

            print('Done with ', file)
        # print(element['location'], element['waypoint_index'], [path[idx][1], path[idx][0]])

    # latitude = sum(p[0] for p in path) / len(path)
    # longitude = sum(p[1] for p in path) / len(path)
    # myMap = folium.Map(location=[latitude, longitude], zoom_start=8)

    # folium.PolyLine(path, color="black", weight=2.5, opacity=1).add_to(myMap)
    # folium.PolyLine(matched_path, color="blue", weight=2.5, opacity=1).add_to(myMap)

    # myMap.save('map.html')


if __name__ == '__main__':
    main()


