import cv2 as open_cv
import numpy as np
#from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE

class CaptureReadError(Exception):
    pass

class MotionDetector:
    LAPLACIAN= 3.4
    DETECT_DELAY= 1

    def __init__(self, video, coordinates, start_frame):
        self.video= video
        self.coordinates_data= coordinates
        self.start_frame= start_frame
        self.bounds= []
        self.mask= []

    def detect_motion(self):
        capture= open_cv.VideoCapture(self.video)
    
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)  

        coordinates_data= self.coordinates_data

        '''
        mask 작업을 위해
        원점을 기준으로 원 안에 정사각형을 만들기 위해 좌표를 설정
        '''
        for p in coordinates_data['data']:
            points= p['coordinates']
            #print(points)
            x= points[0]
            y= points[1]
            d= round(points[2]*(1/ (2**(1/2))))
            coordinates= np.array([[x-d, y-d], [x+d, y-d], [x+d, y+d], [x-d, y+d]])
            rect= open_cv.boundingRect(coordinates)
            #print(rect)
            #print(coordinates)
            new_coordinates= coordinates.copy()
            new_coordinates[:, 0]= coordinates[:, 0]- rect[0]
            new_coordinates[:, 1]= coordinates[:, 1]- rect[1]

            self.bounds.append(rect)

            mask= open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask= mask== 255
            self.mask.append(mask)

        statuses= [False] * len(coordinates_data['data'])
        times= [None] * len(coordinates_data['data'])

        while capture.isOpened():
            result, frame= capture.read()
            if frame is None:
                break
            if not result:
                raise CaptureReadError('Error reading video capture on frame %s' %str(frame))
            
            blurred= open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed= open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)

            new_frame= frame.copy()
            position_in_seconds= capture.get(open_cv.CAP_PROP_POS_MSEC)/ 1000.0

            for index, c in enumerate(coordinates_data['data']):
                status= self.__apply(grayed, index, c)
                #print(times[index])

                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index]= None
                    continue
                
                if times[index] is not None and self.status_changed(statuses, index, status):
                    #print(position_in_seconds- times[index])
                    if position_in_seconds- times[index]>= MotionDetector.DETECT_DELAY:
 
                        statuses[index]= status
                        #print(statuses[index])
                        times[index]= None
                    continue
                
                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index]= position_in_seconds
                    #print(times[index])    # 차가 들어온 시간

            for index, p in enumerate(coordinates_data['data']):
                points= p['coordinates']
                #print(points)
                x= points[0]
                y= points[1]
                d= round(points[2]*(1/ (2**(1/2))))
                coordinates= np.array([[x-d, y-d], [x+d, y-d], [x+d, y+d], [x-d, y+d]])
                
                color= COLOR_GREEN if statuses[index] else COLOR_BLUE
                open_cv.circle(new_frame, (x, y), points[2], color, 1)
                open_cv.imshow(str(self.video), new_frame)
                open_cv.putText(new_frame, str(p["id"] + 1), (x, y), open_cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1, open_cv.LINE_AA)

            open_cv.imshow(str(self.video), new_frame)
            k= open_cv.waitKey(1)
            if k== ord("q"):
                break

        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        points= p['coordinates']
        #print(points)
        x= points[0]
        y= points[1]
        d= round(points[2]*(1/ (2**(1/2))))
        coordinates= np.array([[x-d, y-d], [x+d, y-d], [x+d, y+d], [x-d, y+d]])
        #print(coordinates)

        rect= self.bounds[index]
        #print(rect)

        roi_gray= grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian= open_cv.Laplacian(roi_gray, open_cv.CV_64F)

        status= np.mean(np.abs(laplacian * self.mask[index]))< MotionDetector.LAPLACIAN
        # print(laplacian)
        # print()
        # print(self.mask[index])
        #print(np.mean(np.abs(laplacian * self.mask[index])))
        #print(status)-> 차가 있으면 False 반환
        #plt.imshow(np.abs(laplacian * self.mask[index]))
        #plt.show()

        return status

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status== coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status!= coordinates_status[index]

    


