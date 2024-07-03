import os
import cv2
import numpy as np
import copy


#Calculate dimension
def calc_dimension(screen):
    _,img=screen.read()
    return img.shape


def main():
    lion=cv2.VideoCapture('./videos/lion_roar_2.mp4')
    cam=cv2.VideoCapture(0) #-- (480, 640, 3)
    w,h,_=calc_dimension(cam) #-- (720, 1280, 3)
    green_rgb = np.array([[[8, 243, 27]]],dtype=np.uint8)
    green_hsv = cv2.cvtColor(green_rgb,cv2.COLOR_RGB2HSV)
    lower_range = np.array([green_hsv[0][0][0]-20,100,100])
    upper_range = np.array([green_hsv[0][0][0]+20,255,255])

    while True:
        key = cv2.waitKey(10)
        if key == 27:  
            break


        ret_lion,video=lion.read()
        ret_cam,camera=cam.read()

        if not ret_lion and not ret_cam:
            break

    # Preparation for masking root image (IMAGE WITH GREEN BG)
        # Copy the image for list are mutable
        lion_img=copy.deepcopy(video)
        cam_img=copy.deepcopy(camera)

    # Resize lion image for its smaller
        lion_img = cv2.resize(lion_img,(h,w))


        #Convert to right color domain
        lion_img_hsv=cv2.cvtColor(lion_img,cv2.COLOR_RGB2HSV)
        # cam_img_hsv=cv2.cvtColor(cam_img,cv2.COLOR_RGB2HSV)


        #Perform masking operation with a range between them
        lion_img_hsv=cv2.inRange(lion_img_hsv,lower_range,upper_range)
        #Inverse the image color (BLACK --> WHITE and vice versa)
        lion_img_inv=255-lion_img_hsv


    # Perform cutting process to get the object only part 
    # Added back the object except the green screen and all others are blackened out for masking
        lion_img_mask=cv2.bitwise_or(lion_img,lion_img,mask=lion_img_inv)


    #Create a black space in the camera to add the previous object into 
        temp_img=cv2.bitwise_or(cam_img,cam_img,mask=lion_img_hsv)
    
    #Added both the images into a single one
        final_img=cv2.bitwise_or(temp_img,lion_img_mask)
        
        cv2.imshow('img',final_img)

    cam.release()
    lion.release()
    cv2.destroyAllWindows()



if __name__=='main':
    main()

main()