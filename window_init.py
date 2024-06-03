import cv2
import numpy as np

def create_instruction_window():
    # Create an empty window
    cv2.namedWindow('Hand 2048 Instructions')

    # Create a blank image and then change it to the desired color and size
    background = np.zeros((1000, 800,3), dtype=np.uint8)
    background = cv2.resize(background,(700,600))
    background[:] = (0,170,255) #BGR

    # move the window and put it where needed
    cv2.moveWindow('Hand 2048 Instructions', 570, 40)

    # paste on the background the image in the desired position using transformations, bitwise operators and masking like we did in class
    image = cv2.imread('game_2048\\2048Tiles.png')
    image = cv2.resize(image,None, fx=0.2,fy=0.2)
    img_h, img_w = image.shape[:2]
    src_points=np.array([[0,0],[0,img_h-1],[img_w-1,img_h-1],[img_w-1,0]], dtype=np.float32)
    # define the dest. pts. that can be changed to where we like the top 2048 image to be
    dst_points = np.array([[20,20],[20,img_h+20],[img_w+20,img_h+20],[img_w+20,20]],dtype=np.float32)
    M = cv2.getPerspectiveTransform(src_points,dst_points)
    warped = cv2.warpPerspective(image, M, (background.shape[1],background.shape[0]))
    mask = np.zeros(background.shape, dtype=np.uint8)
    cv2.fillConvexPoly(mask,np.int32(dst_points), (255,255,255))
    mask = cv2.bitwise_not(mask)
    masked_background = cv2.bitwise_and(background,mask)
    instructions = cv2.bitwise_or(masked_background, warped)

    # decorate the instructions image with text
    # put the title
    cv2.putText(instructions, 'Hand 2048',(170,85),cv2.FONT_HERSHEY_SIMPLEX,3,(0,100,255),5)
    cv2.putText(instructions, 'instructions',(250,150),cv2.FONT_HERSHEY_SIMPLEX,2,(0,100,255),2)

    # put the instructions
    cv2.putText(instructions, 'Main Hand Movements:',(15,210),cv2.FONT_HERSHEY_SIMPLEX,1,(108,108,108),1)
    cv2.putText(instructions, '- to move the tiles -> move index finger left, right, down or up (MOVE)',(30,240),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, '- to pause/un-pause the game -> touch thumb point with pinky point (PAUSE)',(30,260),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, '- to enter/exit mouse mode -> touch thumb point with middle point (MOUSE)',(30,280),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, '- to move the mouse -> move index finger in any direction (CIRCLE on index)',(30,300),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, '- to click buttons -> touch thumb point with ring finger point (CLICK!)',(30,320),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, '- to click, hold and move objects -> hold thumb point and ring finger point',(30,340),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)
    cv2.putText(instructions, 'together while moving index finger in any direction (HOLDING)',(52,360),cv2.FONT_HERSHEY_SIMPLEX,0.5,(108,108,108),1)

    # practice the movements here
    cv2.putText(instructions, 'Practice:', (15,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (108,108,108), 1)
    cv2.putText(instructions, 'You can practice the movements here and then proceed to play. To check if', (30,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108,108,108), 1)
    cv2.putText(instructions, 'the movements are correct a writing will appear on the screen. It should', (30,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108,108,108), 1)
    cv2.putText(instructions, 'correspond to what is written in capslock above next to the actions.', (30,470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108,108,108), 1)

    # put the instruction for starting the game
    cv2.putText(instructions, 'Play:', (15,510), cv2.FONT_HERSHEY_SIMPLEX, 1, (108,108,108), 1)
    cv2.putText(instructions, 'If you have understood the instructions and would like to start playing the game', (30,540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108,108,108), 1)
    cv2.putText(instructions, 'please touch thumb point with index point! (PLAY)', (30,560), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108,108,108), 1)

    cv2.imshow('Hand 2048 Instructions',instructions)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
