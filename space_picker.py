import cv2
import pickle

# Define parking space size
width, height = 30, 17

# Load saved parking positions
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

# Use Iriun Webcam (acts as a virtual webcam)
cap = cv2.VideoCapture(2)  # If 0 doesn't work, try 1 or 2

def mouseClick(events, x, y, flags, params):
    global posList
    if events == cv2.EVENT_LBUTTONDOWN:  # Left-click to add a parking space
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:  # Right-click to remove a parking space
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y1 + height:
                posList.pop(i)
                break

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to get video stream. Check Iriun Webcam connection.")
        break

    # Draw rectangles on saved parking positions
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Live Parking", img)
    cv2.setMouseCallback("Live Parking", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
