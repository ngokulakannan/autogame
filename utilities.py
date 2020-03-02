import cv2;

def rotate(image,degree):
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)
    
    M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255,255,255))

    return rotated


