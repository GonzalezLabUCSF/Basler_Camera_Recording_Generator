from pypylon import pylon, genicam
from imageio import get_writer
import sys, time, datetime, numpy, multiprocessing
from recording_cams_script_v1 import record_cam
print("packages imported")
img=pylon.PylonImage()
TLFactory=pylon.TlFactory.GetInstance()
P=multiprocessing.Process
devices=TLFactory.EnumerateDevices()

def find_cams():
    stop_limit=0
    if len(devices) == 0:
            while len(devices) == 0:
                print("No cameras detected")
                stop_limit+=1
                if stop_limit== 3:
                    print("check cables.")
                    quit()
    print("We have "+str(len(devices))+" cameras")
    cameras=pylon.InstantCameraArray(min(len(devices), 2))
    camera_list=[]
    for i, camera in enumerate(cameras):
        camera.Attach(TLFactory.CreateDevice(devices[i]))
        camera.Open()
        x=str(camera.GetDeviceInfo().GetIpAddress())
        print("Found device ", camera.GetDeviceInfo().GetModelName(), "with ",x, "address")
find_cams()
time.sleep(20)
sys.exit(1)
