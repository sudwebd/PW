import cv2
import sys
import time
import math
import numpy as np
if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[2]
    minor_ver = 4
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()

    # Read video
    video = cv2.VideoCapture(0)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    s1 = time.time();
    centroid = (bbox[0]+(bbox[2]/2),bbox[1]+(bbox[3]/2))
    relpos = (np.size(frame, 0),np.size(frame, 1)/2)
    d1 = math.sqrt(((centroid[0] - relpos[1])*(centroid[0] - relpos[1])) + ((centroid[1] - relpos[0])*(centroid[1] - relpos[0])))
    loop = 0;
    sp = 0;
    t1 = time.time()
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            if(loop%5==0):
                centroid = (bbox[0]+(bbox[2]/2),bbox[1]+(bbox[3]/2))
                d2 = math.sqrt(((centroid[0] - relpos[1])*(centroid[0] - relpos[1])) + ((centroid[1] - relpos[0])*(centroid[1] - relpos[0])))
                speed = (d1 - d2)/(time.time() - t1)
                t1 = time.time()
                d1 = d2
                sp = speed
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, "Speed: " + str(sp), (100, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2) 
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        cv2.imshow("Tracking", frame)
        loop = loop + 1
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
