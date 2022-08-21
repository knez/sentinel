import os
import cv2
import numpy as np
import argparse
import logging
import requests
import yaml
import datetime


# init mobilenet SSD settings
RESIZED_DIMENSIONS = (300, 300) # Dimensions that SSD was trained on. 
IMG_NORM_RATIO = 0.007843 # In grayscale a pixel can range between 0 and 255

# load the pre-trained neural network
neural_network = cv2.dnn.readNetFromCaffe('trained_model/MobileNetSSD_deploy.prototxt.txt', 
        'trained_model/MobileNetSSD_deploy.caffemodel')

# neural network classes to identify
classes =  [
            "background", "aeroplane", "bicycle", "bird", "boat", "bottle", 
            "bus", "car", "cat", "chair", "cow", 
            "diningtable",  "dog", "horse", "motorbike", "person", 
            "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

# stores sentinel main settings
config = None

def init_config():
    with open('settings.yml', 'r') as stream:
        try:
            global config
            config = yaml.safe_load(stream)
            logging.debug('Config file successfully initialized')
        except yaml.YAMLError as exc:
            logging.error(exc)
            exit(1)


# upload file to configured dashboard
def send_file(save_name):
    upload_url = config['dashboard']['url']
    file = {'video_file': ('save_name', open(save_name, 'rb'))}
    response = requests.post(upload_url, files=file)
    if response.status_code == 200:
        logging.debug(f'File {save_name} uploaded to {upload_url}')
    else:
        logging.error('Error occured during uploading')
    # delete the file
    os.remove(save_name)
    logging.debug(f'Deleting file {save_name}')


def detect_kind(frame):
    frame_blob = cv2.dnn.blobFromImage(cv2.resize(frame, RESIZED_DIMENSIONS), 
                     IMG_NORM_RATIO, RESIZED_DIMENSIONS, 127.5)    
    # Set the input for the neural network
    neural_network.setInput(frame_blob)

    # Predict the objects in the image
    neural_network_output = neural_network.forward()

    # Put the bounding boxes around the detected objects
    for i in np.arange(0, neural_network_output.shape[2]):            
        confidence = neural_network_output[0, 0, i, 2]
        # Confidence must be at least 50%       
        if confidence > 0.50:
            idx = int(neural_network_output[0, 0, i, 1]) 
            label = classes[idx]  
            return label         
        else:
            return 'unknown'


def create_save_name(cap):
    date_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    save_name = 'video-' + date_now + '.mp4'
    # get the video frame height and width
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # define codec and create VideoWriter object
    out = cv2.VideoWriter(
        save_name,
        cv2.VideoWriter_fourcc(*'mp4v'), fps / 2, 
        (frame_width, frame_height)
    )
    logging.debug(f"Saving video footage into {save_name}")
    return save_name, out


def detect_location(x, y, cap):
    w = int(cap.get(3))
    h = int(cap.get(4))

    if x < w/2 and y > h/2:
        return 'bottom-left'
    if x < w/2 and y < h/2:
        return 'top-left'
    if x >= w/2 and y > h/2:
        return 'bottom-right'
    if x >= w/2 and y < h/2:
        return 'top-right'  
    return 'unknown'


def main_loop(cap):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap_frames = 10 * fps / 2 # capture 10sec video
    background = None
    frame_count = 0
    consecutive_frame = 2
    i = cap_frames
    is_capturing = False

    while (cap.isOpened()):
        check, frame = cap.read()
        if check == True:

            orig_frame = frame.copy()

            if background is None:
                # set background to first frame
                background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_count += 1
            # IMPORTANT STEP: convert the frame to grayscale first
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []
            # find the difference between current frame and base frame
            frame_diff = cv2.absdiff(gray, background)
            # thresholding to convert the frame to binary
            ret, thres = cv2.threshold(frame_diff, 40, 255, cv2.THRESH_BINARY)
            # dilate the frame a bit to get some more white area...
            # ... makes the detection of contours a bit easier
            dilate_frame = cv2.dilate(thres, None, iterations=2)
            # append the final result into the `frame_diff_list`
            frame_diff_list.append(dilate_frame)
            # if we have reached `consecutive_frame` number of frames
            if len(frame_diff_list) == consecutive_frame:
                # add all the frames in the `frame_diff_list`
                sum_frames = sum(frame_diff_list)
                # find the contours around the white segmented areas
                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)            
                movement = False
                for contour in contours:
                    # continue through the loop if contour area is less than 500...
                    # ... helps in removing noise detection
                    if cv2.contourArea(contour) < 10000:
                        continue

                    movement = True
                    # get the xmin, ymin, width, and height coordinates from the contours
                    (x, y, w, h) = cv2.boundingRect(contour)
                    location = detect_location(x, y, cap)
                    # draw the bounding boxes
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if movement and not is_capturing:
                    save_name, out = create_save_name(cap)
                    out.write(orig_frame)
                    is_capturing = True
                elif is_capturing:
                    if i != 0:
                        out.write(orig_frame)
                        i = i - 1
                        # wait a little before detecting
                        if i == cap_frames - 25: 
                            kind = detect_kind(frame)
                            logging.info(f"Detected new object: {kind}, location: {location}")
                    else:
                        is_capturing = False
                        i = cap_frames
                        send_file(save_name)

                if args['debug']:
                    cv2.imshow('Detected Objects', frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        else:
            break


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='show live camera window',
                        dest='debug', action='store_true', required=False, default=False)
    return vars(parser.parse_args())


if __name__ == '__main__':
    # parse arguments
    args = parse_arguments()
    # configure logging level
    if args['debug']:
        logging.basicConfig(level=logging.DEBUG)
    else: 
        logging.basicConfig(level=logging.INFO)

    # load app main settings
    init_config()

    # capture camera input
    cap = cv2.VideoCapture(0)
    # check if the video opened successfully
    if (cap.isOpened() == False): 
        logging.error("Error opening video file")
        exit(1)
    else:
        logging.debug("Capture started")
        main_loop(cap)

    logging.debug("Capture stopped")
    cap.release()
    cv2.destroyAllWindows()
