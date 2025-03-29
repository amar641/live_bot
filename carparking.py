import cv2
import pickle
import cvzone
import numpy as np
import json
from probability import calculate_probability, load_database, save_database

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 30, 17 

def checkParkingSpace(imgPro, img):
    free_spaces = 0
    occupied_spaces = 0

    for idx, pos in enumerate(posList):
        try:
            x, y = map(int, pos)
            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)

            threshold = 100  
            
            if count < threshold:  
                color = (0, 255, 0)  
                free_spaces += 1
            else:  
                color = (0, 0, 255)  
                occupied_spaces += 1

        
            cv2.rectangle(img, (x, y), (x + width, y + height), color, 2)

         
            label = f"A{idx + 1}"
            cvzone.putTextRect(img, label, (x + 5, y + height + 15), scale=0.5,
                               thickness=1, offset=3, colorR=color)
        
        except Exception as e:
            print(f"Error processing parking space {pos}: {e}")
    
    return free_spaces, occupied_spaces

cap = cv2.VideoCapture(2)  

data = load_database()
total_spaces = data["parking_lot"]["total_spaces"]

while True:
    success, img = cap.read()
    if not success:
        print("Camera feed not available.")
        break 

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    free_spaces, occupied_spaces = checkParkingSpace(imgDilate, img)  
    probability = calculate_probability()

    
    data["parking_lot"]["free_spaces"] = free_spaces
    data["parking_lot"]["occupied_spaces"] = occupied_spaces
    data["parking_lot"]["probability"] = probability
    save_database(data)

  
    print(f"Total Spaces: {total_spaces}, Free: {free_spaces}, Occupied: {occupied_spaces}, Probability: {probability}%")

   
    cvzone.putTextRect(img, f"Total: {total_spaces}  Occupied: {occupied_spaces}  Prob: {probability}%", 
                       (50, 50), scale=1, thickness=2, offset=5, colorR=(255, 0, 0))
    
    cv2.imshow("Live Parking", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break  

cap.release() 
cv2.destroyAllWindows()
