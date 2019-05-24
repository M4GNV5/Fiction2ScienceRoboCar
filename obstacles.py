import cv2, sys

img = cv2.imread(sys.argv[1])
colored = img
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask1 = cv2.inRange(img, (0, 30, 30), (10, 255, 255))
mask2 = cv2.inRange(img, (170, 30, 30), (180, 255, 255))

img = cv2.bitwise_or(mask1, mask2)
contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

def isSign(contour):
    area = cv2.contourArea(contour)
    if area < 2500:
        return False

    x, y, w, h = cv2.boundingRect(contour)

    # check if the bounding rect is approx a square
    if abs(1 - w / h) > 0.1:
        return False

    return True

totalBlockerWidth = 0
def couldBeBlock(contour):
    global totalBlockerWidth

    area = cv2.contourArea(contour)
    if area < 3000:
        return False

    x, y, w, h = cv2.boundingRect(contour)

    # check if the bounding rect is approx a 2x=1y rect
    if abs(1 - (w / 2) / h) > 0.2:
        return False

    totalBlockerWidth += w
    return True

signContours = [x for x in filter(isSign, contours)]
blockerContours = [x for x in filter(couldBeBlock, contours)]

sys.stdout.write(sys.argv[1] + " - ")
if totalBlockerWidth > 400:
    print("rb")
elif len(signContours) > 0:
    print("stop")
else:
    print("nothing")

#img = colored
#cv2.drawContours(img, signContours, -1, (255, 0, 0), 3)
#cv2.drawContours(img, blockerContours, -1, (0, 255, 0), 3)

#cv2.imshow("output", img)
#key = cv2.waitKey(300) & 0xff
