# GPS_Track_OpenStreetMap
**Toolbox with GPS tracks from OSM (OpenStreetMap)**

### RetrieveTrackOSM.py: Retrieve GPS trackpoints from OpenStreetMap in a given bounding-box
- Line 54: User-specified range of bounding box 
  - Visualization of OSM GPS: https://www.openstreetmap.org/#map=12/40.7463/-73.9644&layers=G
  - Find lat and lng via the link, https://www.latlong.net/
- Line 82: User-specified max number of GPS tracks from 0.25x0.25 bounding box
  - Assume we set <code>track_count_per_area</code> to 100 and <code>left</code> & <code>right</code> & <code>bottom</code> & <code>top</code> to -70.5 & -70 & 40 & 40.75, then we will eventually have 2x3=6 sub bounding-box and 100x6=600 GPS tracks

### MapMatchOSM.py: Match GPS trackpoints to OpenStreetMap
- **Due to the contraints of the demo server from OSRM (http://project-osrm.org/), please setup local server before running the script**

- **Step-by-step instruction: https://gist.github.com/AlexandraKapp/e0eee2beacc93e765113aff43ec77789**

- **The map of Northeast region of North America can be downloaded from http://download.geofabrik.de/north-america.html**

- **Docker Install (Windows): https://docs.docker.com/desktop/windows/install/**

- **Enable HYPER-V: https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v**

Notes (necessary for our experiments):
- Increase RAM: Settings -> Resources -> ADVANCED -> Memory
- It is most likely to have "[INPUT ERROR]" when first time running <code>docker run -t -v c:/docker:/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/us-northeast-latest.osm.pbf</code>. Not a big deal - Drag <code>us-northeast-latest.osm.pbf</code> into <code>c:/docker</code> (or under the other FILE SHARING folder you setup earlier) which was just created by the command, and Run the command again
- Add max-matching-size param: <code>docker run --name osrm -t -i -p 5000:5000 -v c:/docker:/data osrm/osrm-backend osrm-routed --max-matching-size 50000 --algorithm mld /data/us-northeast-latest.osrm</code>
