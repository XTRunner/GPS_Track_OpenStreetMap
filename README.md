# GPS_Track_OpenStreetMap
**Toolbox with GPS tracks from OSM (OpenStreetMap)**

### RetrieveTrackOSM.py: Retrieve GPS trackpoints from OpenStreetMap in a given bounding-box
- Line 54: User-specified range of bounding box -- Visualization of OSM GPS: https://www.openstreetmap.org/#map=12/40.7463/-73.9644&layers=G
- Line 82: User-specified max number of GPS tracks from 0.25*0.25 bounding box -- Find lat and lng via the link, https://www.latlong.net/

### MapMatchOSM.py: Match GPS trackpoints to OpenStreetMap
**Due to the contraints of the demo server from OSRM (http://project-osrm.org/), please setup local server before running the script**

**Step-by-step instruction: https://gist.github.com/AlexandraKapp/e0eee2beacc93e765113aff43ec77789**

**Northeast region of North America can be downloaded from http://download.geofabrik.de/north-america.html**

**Docker Install (Windows): https://docs.docker.com/desktop/windows/install/**

**Enable HYPER-V: https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v**

Notes:
- Increase RAM: Settings -> Resources -> ADVANCED -> Memory
- It is most likely to have "[INPUT ERROR]" when you first time running <code>docker run -t -v c:/docker:/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/us-northeast-latest.osm.pbf</code>. Not a big deal -- Drag us-northeast-latest.osm.pbf into c:/docker (which was just created by the command), and Run the command again
- Add max-matching-size param: <code>docker run --name osrm -t -i -p 5000:5000 -v c:/docker:/data osrm/osrm-backend osrm-routed --max-matching-size 50000 --algorithm mld /data/us-northeast-latest.osrm</code>
