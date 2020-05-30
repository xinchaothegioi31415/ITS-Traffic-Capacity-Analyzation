from traffic_capacity_2 import *
from multiprocessing.pool import ThreadPool
import firebase_admin

# Notifying starting system
print("Starting ITS system...")
# init
path_folder = "stream videos"
video_names = ["road1.mp4", "road2.mp4", "road3.mp4", "road4.mp4", "road5.mp4", "road6.mp4"]
stream_url = ["%s/%s" % (path_folder, name) for name in video_names]

AREA_PTS1 = np.array([[1008,290],[1118,282],[982,702],[414,709]])
AREA_PTS2 = np.array([[725,326],[819,359],[233,715],[23,607],[641,381],[687,358]])
AREA_PTS3 = np.array([[379,345],[484,346],[964,709],[513,708]])
AREA_PTS4 = np.array([[917,383],[993,401],[827,706],[420,707]])
AREA_PTS5 = np.array([[1077,194],[1162,216],[934,704],[130,709],[36,576]])
AREA_PTS6 = np.array([[931,74],[945,118],[8,563],[4,319],[481,145]])
AREAS_PTS = [AREA_PTS1, AREA_PTS2, AREA_PTS3, AREA_PTS4, AREA_PTS5, AREA_PTS6]

camera_names = ["BuiVanDanh", "TranHungDao", "LeTrieuKiet", "NguyenThaiHoc", "TonDucThang", "LeVanNhung"]

p = ThreadPool(processes=1)

p.starmap(runCamera, zip(stream_url, camera_names, AREAS_PTS))

p.close()
p.join()