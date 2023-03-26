import re

class ReadFile():

    def __init__(self):
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


        self.pattern = r'(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s+(\d+)\s+(\d+)\s+([A-Z]+)\s+(.+)'

        self.file_data = None


    def read_file_execute(self,file_path_received):

        #open the file and read lines as a list
        self.file_path=file_path_received
        with open(self.file_path, 'r') as file:
            self.file_data = file.readlines()




    def read_file_execute_fps(self):
        previous_timestamp = 0
        offset = 0

        for line in self.file_data:

            if"FPS" in line:
                # Extract relevant information from log line
                match = re.match(self.pattern, line)
                if match:
                    print("MatchFound)")
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
                    fps_match=re.match(r"FPS=(\d+)",payload)
                    fps=float(fps_match.group(1))


                    # Calculate timestamp
                    timestamp = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000 + offset

                    # Check if current timestamp is more than 100000 less than previous
                    if timestamp < previous_timestamp - 100000:
                        offset += 24 * 60 * 60 * 1000
                        timestamp += 24 * 60 * 60 * 1000

                    # Update previous timestamp to current value
                    previous_timestamp = timestamp

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
                    self.timestamp_list.append(float(timestamp))
                    self.fps_list.append(fps)




    def read_logs_with_tags(self,tag_list):
        self.filter_log=[]

        for line in self.file_data:
            for tag in tag_list:
                if tag in line:
                    self.filter_log.append(line)

    def return_filtered_logs(self):
        return self.filter_log









#default main funcion

if __name__ == '__main__':
    RD=ReadFile()
    RD.read_file_execute_fps()

