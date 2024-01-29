from pypylon import pylon, genicam
from imageio import get_writer
import sys, time, datetime, os, cv2,numpy
#Recording Function
def record_cam(CAMERA,WRITER,frame_number,start_recording,grab_file_path):
    file=open(grab_file_path,"w")
    file.write("started recording at"+start_recording+"\n")
    acquired_images=0
    CAMERA.StartGrabbing(pylon.GrabStrategy_OneByOne)
    file=open(grab_file_path,"w")
    while True:
        try:
            grabResult= CAMERA.RetrieveResult(40,pylon.TimeoutHandling_ThrowException)
            
            if grabResult.GrabSucceeded():
                file.write(str(time.time())+"\n")
                #print(grabResult.Array)
                WRITER.append_data(cv2.cvtColor(grabResult.Array,cv2.COLOR_BAYER_RG2RGBA))
                grabResult.Release()
                acquired_images += 1
                if acquired_images == frame_number:
                    CAMERA.StopGrabbing()
                    CAMERA.Close()
                    break
                continue
            else:
                continue
        except:
            continue

#Folders Function
def create_camera_folder(camera_name):
    if camera_name not in os.listdir():
        os.mkdir(camera_name)
        os.mkdir(camera_name+"/grab_timestamps")
        os.mkdir(camera_name+"/recordings")
        print(f"Upload {camera_name} PFS file to its folder.")

#Creates and attaches a device based on IP address
def Find_my_cam_by_IP():
    img=pylon.PylonImage()
    TLFactory=pylon.TlFactory.GetInstance()
    ip_address = '192.168.0.100'
    print(f"Getting camera at {ip_address}")
    ptl = TLFactory.CreateTl('BaslerGigE')
    empty_camera_info = ptl.CreateDeviceInfo()
    empty_camera_info.SetPropertyValue('IpAddress', ip_address)
    camera_device = TLFactory.CreateDevice(empty_camera_info)
    camera = pylon.InstantCamera(camera_device)
    camera.Open()
    camera_name=str(camera.GetDeviceInfo().GetModelName())+"_"+str(camera.GetDeviceInfo().GetSerialNumber())
    create_camera_folder(camera_name)
    nodeFile=camera_name+"/"+f"{camera_name}.pfs"
    pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
    print("Configured device "+ camera_name)
    return camera

    
def create_files_and_writers(device):
    grab_file_path={}
    camera_name=str(device.GetDeviceInfo().GetModelName())+"_"+str(device.GetDeviceInfo().GetSerialNumber())
    file_name =camera_name+"_"+str(datetime.datetime.now())
    for t in [":"," ","-","."]:
        file_name=file_name.replace(t,"_")
    for t in [":"," "]:
        camera_name=camera_name.replace(t,"_")
    print(camera_name)
    video_file_path=camera_name+"/recordings/"+file_name+".mp4"
    grab_file_path=camera_name+"/grab_timestamps/"+file_name+"grab.txt"
    writer=get_writer(video_file_path,mode="?")
    return grab_file_path, writer

camera=Find_my_cam_by_IP()
grab_file_path, writer=create_files_and_writers(camera)
acquired_images=0
print("Cam Recording")
start_recording=str(time.time())
# print(start_recording)
full_day=2851200
record_cam(camera,writer,700,start_recording,grab_file_path)

#camera.Close()
print("done recording")
sys.exit(1)