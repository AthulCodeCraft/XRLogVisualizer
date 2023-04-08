import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication
import re
from  math import *
import re
import numpy as np
from datetime import datetime

pattern = re.compile(r'^(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{3}) (\d+) (\d+) (\S+) (.*)$')

class ReadFile(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.file_path = 'r.txt'

        self.day_list = []
        self.month_list = []
        self.hour_list = []
        self.minute_list = []
        self.second_list = []
        self.millisecond_list = []
        self.process_id_list = []
        self.sub_id_list = []
        self.tag_list = []
        self.payload_list = []
        self.timestamp_list = []
        self.fps_list = []
        self.filter_log=[]
        self.battery_level_list=[]
        self.x_list = []
        self.y_list = []
        self.z_list = []


        self.logcat_log_pattern = r'(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s+(\d+)\s+(\d+)\s+([A-Z]+)\s+(.+)'

        self.htp_xml_pattern = r"rx='(-?\d+\.\d+)' ry='(-?\d+\.\d+)' rz='(-?\d+\.\d+)' rw='(-?\d+\.\d+)' timestamp='(\d+)' x='(-?\d+\.\d+)' y='(-?\d+\.\d+)' z='(-?\d+\.\d+)' itr='(\d+)' technique='(-?\d+\.\d+)'"
        self.exposure_ns_pattern = r"exposureNs='(\d+)'"
        self.iso_gain_pattern =  r"isoGain='(\d+)'"
        self.metainfo_timestamp_pattern = r"timestamp='(\d+)'"
        self.metainfo_timestamp_list = []
        self.isogain_list = []
        self.exposure_ns_list = []
        self.tracking_camera_fps_list= []


        self.file_data = None

        #variables for htp #####################
        self.htp_rx_list=[]
        self.htp_ry_list=[]
        self.htp_rz_list=[]
        self.htp_rw_list=[]
        self.htp_timestamp_list=[]
        self.htp_x_list=[]
        self.htp_y_list=[]
        self.htp_z_list=[]
        self.htp_itr_list=[]
        self.htp_technique_list=[]
        self.htp_maximum_value=None
        self.htp_minimum_value=None
        self.htp_pitch_list=[]
        self.htp_roll_list=[]
        self.htp_yaw_list=[]



        ########################################
        


    def read_file_execute(self,file_path_received):

        #open the file and read lines as a list
        self.file_data=None
        self.file_path=file_path_received
        with open(self.file_path, 'r') as file:
            self.file_data = file.readlines()


    def set_variables_zero(self):
        self.day_list = []
        self.month_list = []
        self.hour_list = []
        self.minute_list = []
        self.second_list = []
        self.millisecond_list = []
        self.process_id_list = []
        self.sub_id_list = []
        self.tag_list = []
        self.payload_list = []
        self.timestamp_list = []
        self.fps_list = []
        self.battery_level_list=[]
        self.x_list= []
        self.y_list= []
        self.z_list= []


    # compile regular expression pattern
    pattern = re.compile(r'^(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.(\d{3}) (\d+) (\d+) (\S+) (.*)$')

    def read_file_execute_fps(self):
        previous_timestamp = 0
        offset = 0
        self.set_variables_zero()

        # Get total number of lines
        total_lines = len(self.file_data)
        current_line = 0

        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")


        for line in self.file_data:

            current_line += 1

            if "FPS" in line:

                # Extract relevant information from log line
                match = re.match(self.logcat_log_pattern, line)
                if match:

                    day = int(match.group(1))
                    month = int(match.group(2))
                    hour = int(match.group(3))
                    minute = int(match.group(4))
                    second = int(match.group(5))
                    millisecond = int(match.group(6))
                    process_id = int(match.group(7))
                    sub_id = int(match.group(8))
                    tag = match.group(9)
                    payload = match.group(10)
                    fps_match = re.match(r"FPS=(\d+)", payload)
                    fps = float(fps_match.group(1))

                    # Calculate timestamp
                    timestamp = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000 + offset

                    # Check if current timestamp is more than 100000 less than previous
                    if timestamp < previous_timestamp - 100000:
                        offset += 24 * 60 * 60 * 1000
                        timestamp += 24 * 60 * 60 * 1000

                    # Update previous timestamp to current value
                    previous_timestamp = timestamp

                    # Update progress bar

                    progress_value = int(current_line / total_lines * 100)
                    print(current_line)
                    self.parent.progress_bar_read.setValue(progress_value)

                    # Do whatever processing you need with the extracted information here
                    # print(f"Date: {day}-{month}, Timestamp: {timestamp}, Process ID: {process_id}, Sub ID: {sub_id}, Tag: {tag}, Payload: {payload}")

                    self.day_list.append(day)
                    self.month_list.append(month)
                    self.hour_list.append(hour)
                    self.minute_list.append(minute)
                    self.second_list.append(second)
                    self.millisecond_list.append(millisecond)
                    self.process_id_list.append(process_id)
                    self.sub_id_list.append(sub_id)
                    self.tag_list.append(tag)
                    self.payload_list.append(payload)

                    self.fps_list.append(fps)
                    self.timestamp_list.append(timestamp)

        self.parent.progress_bar_read.setValue(100)
        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: ##67ff67;}")


    def read_logs_with_tags(self,tag_list):
        self.filter_log = []
        for line in self.file_data:
            matched_tags = []
            for tag in tag_list:
                if tag in line:
                    matched_tags.append(tag)

            if len(matched_tags) > 1:
                # There are multiple matched tags, find the one with more words
                max_length = 0
                max_tag = None
                for tag in matched_tags:
                    length = len(tag.split())
                    if length > max_length:
                        max_length = length
                        max_tag = tag
                self.filter_log.append(line.replace(max_tag, f"{max_tag}"))
            elif len(matched_tags) == 1:
                # Only one matched tag
                self.filter_log.append(line)

    def return_filtered_logs(self):
        return self.filter_log


    def read_file_execute_batterylevel(self):

        self.set_variables_zero()
        previous_timestamp = 0
        offset = 0

        for line in self.file_data:

            if "BATTERY LEVEL" in line:
                # Extract relevant information from log line
                match = re.match(self.logcat_log_pattern, line)
                if match:

                    day = int(match.group(1))
                    month = int(match.group(2))
                    hour = int(match.group(3))
                    minute = int(match.group(4))
                    second = int(match.group(5))
                    millisecond = int(match.group(6))
                    process_id = int(match.group(7))
                    sub_id = int(match.group(8))
                    tag = match.group(9)
                    payload = match.group(10)
                    battery_match = re.match(r"BATTERY LEVEL=(\d+)", payload)
                    blevel = float(battery_match.group(1))


                    # Calculate timestamp
                    timestamp = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000 + offset

                    # Check if current timestamp is more than 100000 less than previous
                    if timestamp < previous_timestamp - 100000:
                        offset += 24 * 60 * 60 * 1000
                        timestamp += 24 * 60 * 60 * 1000

                    # Update previous timestamp to current value
                    previous_timestamp = timestamp


                    # Calculate timestamp
                    self.battery_level_list.append(float(blevel))
                    self.timestamp_list.append(float(timestamp))

    def read_file_execute_headpose(self):

        self.set_variables_zero()
        previous_timestamp = 0
        offset = 0


        for line in self.file_data:
            if"POSE: x" in line:
                match = re.match(self.logcat_log_pattern, line)
                if match:
                    day = int(match.group(1))
                    month = int(match.group(2))
                    hour = int(match.group(3))
                    minute = int(match.group(4))
                    second = int(match.group(5))
                    millisecond = int(match.group(6))
                    process_id = int(match.group(7))
                    sub_id = int(match.group(8))
                    tag = match.group(9)
                    payload = match.group(10)
                    #find x,y,z from the pattern RAW POSE: x=0.1 y=0.5 z=0.8


                    headpose_match = re.search(r'RAW POSE: x=(-?\d+\.\d+)\s+y=(-?\d+\.\d+)\s+z=(-?\d+\.\d+)', payload)
                    x = float(headpose_match.group(1))
                    y = float(headpose_match.group(2))
                    z = float(headpose_match.group(3))

                    self.x_list.append(x)
                    self.y_list.append(y)
                    self.z_list.append(z)

                    timestamp = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000 + offset

                    # Check if current timestamp is more than 100000 less than previous
                    if timestamp < previous_timestamp - 100000:
                        offset += 24 * 60 * 60 * 1000
                        timestamp += 24 * 60 * 60 * 1000

                    # Update previous timestamp to current value
                    previous_timestamp = timestamp


                    # Calculate timestamp

                    self.timestamp_list.append(float(timestamp))

    def clear_htp_variables(self):
        self.htp_rx_list=[]
        self.htp_ry_list=[]
        self.htp_rz_list=[]
        self.htp_rw_list=[]
        self.htp_x_list=[]
        self.htp_y_list=[]
        self.htp_z_list=[]
        self.htp_technique_list=[]
        self.htp_timestamp_list=[]
        self.htp_pitch_list=[]
        self.htp_yaw_list=[]
        self.htp_roll_list=[]


    def read_head_tracking_pose_xml(self):
        print("htp file is read")
        self.clear_htp_variables()
        total_lines = len(self.file_data)
        current_line = 0
        htp_match_flag= False
        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")

        for line in self.file_data:
            current_line += 1
            matches = re.search(self.htp_xml_pattern, line)

            if matches:
                htp_match_flag=True

                htp_rx, htp_ry, htp_rz, htp_rw = map(float, matches.group(1, 2, 3, 4))
                htp_x, htp_y, htp_z = map(float, matches.group(6, 7, 8))
                htp_technique = float(matches.group(10))
                htp_timestamp = int(matches.group(5))

                htp_pitch = atan2(2 * (htp_rw * htp_rx + htp_ry * htp_rz), 1 - 2 * (htp_rx * htp_rx + htp_ry * htp_ry))
                htp_yaw = asin(2 * (htp_rw * htp_ry - htp_rz * htp_rx))
                htp_roll = atan2(2 * (htp_rw * htp_rz + htp_rx * htp_ry), 1 - 2 * (htp_ry * htp_ry + htp_rz * htp_rz))



                progress_value = int(current_line / total_lines * 100)

                self.parent.progress_bar_read.setValue(progress_value)


                self.htp_rx_list.append(htp_rx)
                self.htp_ry_list.append(htp_ry)
                self.htp_rz_list.append(htp_rz)
                self.htp_rw_list.append(htp_rw)
                self.htp_x_list.append(htp_x)
                self.htp_y_list.append(htp_y)
                self.htp_z_list.append(htp_z)
                self.htp_technique_list.append(htp_technique)
                self.htp_timestamp_list.append(htp_timestamp)
                self.htp_pitch_list.append(htp_pitch)
                self.htp_yaw_list.append(htp_yaw)
                self.htp_roll_list.append(htp_roll)
                #find the maximum value of multiple list






        if htp_match_flag==True:
            self.parent.progress_bar_read.setValue(100)
            self.htp_maximum_value=max(max(self.htp_x_list),max(self.htp_y_list),max(self.htp_z_list))
            self.htp_minimum_value=min(min(self.htp_x_list),min(self.htp_y_list),min(self.htp_z_list))



        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: ##67ff67;}")





    def clear_metainfo_variables(self):
        self.metainfo_timestamp_list=[]
        self.isogain_list=[]
        self.exposure_ns_list=[]
        self.tracking_camera_fps_list = []





    def read_meta_info_xml(self):

        self.clear_metainfo_variables()
        total_lines = len(self.file_data)
        current_line = 0
        metainfo_match_flag= False
        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")
        previous_timestamp=0

        for line in self.file_data:
            current_line += 1

            exposure_ns_match = re.search(self.exposure_ns_pattern, line)
            io_gain_match = re.search(self.iso_gain_pattern, line)
            timestamp_match = re.search(self.metainfo_timestamp_pattern, line)

            if (timestamp_match):
                print("Metainfo match found")

                metainfo_match_flag=True
                exposure_ns = int(exposure_ns_match.group(1))
                iso_gain = int(io_gain_match.group(1))
                timestamp = int(timestamp_match.group(1))

                tracking_camera_fps = float(1000000000 / (timestamp - previous_timestamp))

                print(tracking_camera_fps)






                progress_value = int(current_line / total_lines * 100)
                self.parent.progress_bar_read.setValue(progress_value)

                self.exposure_ns_list.append(exposure_ns)
                self.isogain_list.append(iso_gain)
                self.metainfo_timestamp_list.append(timestamp)
                self.tracking_camera_fps_list.append(tracking_camera_fps)

                previous_timestamp = timestamp

                #find the maximum value of multiple list






        if metainfo_match_flag==True:
            self.parent.progress_bar_read.setValue(100)
            self.metainfo_exposure_maximum_value=max(self.exposure_ns_list)
            self.metainfo_exposure_minimum_value=min(self.exposure_ns_list)
            self.metainfo_iso_gain_maximum_value=max(self.isogain_list)
            self.metainfo_iso_gain_minimum_value=min(self.isogain_list)


        self.parent.progress_bar_read.setStyleSheet("QProgressBar::chunk {background-color: ##67ff67;}")

#default main funcion

if __name__ == '__main__':
    RD=ReadFile()
    RD.read_file_execute_fps()

