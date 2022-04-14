import cv2 as open_cv
import numpy as np
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE

class CaptureReadError(Exception):
    pass

class MotionDetector:
    LAPLACIAN= 1.4
    DETECT_DELAY= 1

    def __init__(self, video, coordinates, start_frame):
        self.video= video
        self.coordinates_data= coordinates
        self.start_frame= start_frame
        # self.contours= []
        # self.mask= []

    def detect_motion(self):
        capture= open_cv.VideoCapture(self.video)
        #print(capture)
        #print((np.zeros_like(capture.read()[1]).shape)) # shape= (?, ?, 3)
    
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)  

        '''
        coordinates= data_file에서 읽어 온 points
        '''
        coordinates_data= self.coordinates_data

        '''
        비디오가 열려있는 동안 작업

        JSON 파일에서 읽어 온 points에서 ids(원 번호), 좌표, 반지름을 변수로 받아서 
        원을 그리고 그 안에 번호를 그려줍니다.

        q 또는 Q를 누르면 while 문이 종료되고 그 후에 영상이 종료됩니다.
        '''
        while capture.isOpened():
            result, frame= capture.read()
            if frame is None:
                break
            if not result:
                raise CaptureReadError('Error reading video capture on frame %s' %str(frame))
            
            new_frame= frame.copy()
            for p in coordinates_data['coordinates']:
                ids= p['id']
                x, y= p['x'], p['y']
                r= p['r']

                open_cv.circle(new_frame, (x, y), r, COLOR_BLUE, 1)
                open_cv.putText(new_frame, str(ids), (x, y), open_cv.FONT_HERSHEY_SIMPLEX, 1, COLOR_WHITE, 1)

            open_cv.imshow(str(self.video), new_frame)
            k= open_cv.waitKey(1)& 0xFF
            if k== ord("q"):
                break

        capture.release()
        open_cv.destroyAllWindows()

    #     for p in coordinates_data['coordinates']:
    #         coordinates= self._coordinates(p)
    #         #print(coordinates)

    #         self.contours.append(coordinates)

    #         mask= open_cv.circle(m, (p['x'], p['y']), p['r'], (255,255,255), -1)
    #         #print(mask, mask.shape) # shape= (?, ?, 3)

    #         mask= mask== 255
    #         self.mask.append(mask)
    #         #print(self.mask) # T/F로 shape은 위와 동일

    #     statuses= [False] * len(coordinates_data['coordinates'])
    #     times= [None] * len(coordinates_data['coordinates'])

    #     while capture.isOpened():
    #         result, frame= capture.read()
    #         if frame is None:
    #             break

    #         if not result:
    #             raise CaptureReadError("Error reading video capture on frame %s" % str(frame))
            
    #         blurred= open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
    #         grayed= open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
    #         new_frame= frame.copy()

    #         position_in_seconds= capture.get(open_cv.CAP_PROP_POS_MSEC)/ 1000.0
        
    #     for index, c in enumerate(coordinates_data['coordinates']):
    #         status= self.__apply(grayed, index, c)
        
    #         if times[index] is not None and self.same_status(statuses, index, status):
    #             times[index]= None
    #             continue
            
    #         if times[index] is not None and self.status_changed(statuses, index, status):
    #             if position_in_seconds- times[index]>= MotionDetector.DETECT_DELAY:
                    
    #                 statuses[index]= status
    #                 times[index]= None
    #             continue
            
    #         if times[index] is None and self.status_changed(statuses, index, status):
    #             times[index]= position_in_seconds

    #         for index, p in enumerate(coordinates_data)['coordinates']:
    #             coordinates= self._coordinates(p)
                
    #             color= COLOR_GREEN if statuses[index] else COLOR_BLUE
    #             draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

    #         open_cv.imshow(str(self.video), new_frame)
    #         k= open_cv.waitKey(1)
    #         if k== ord("q"):
    #             break

    #     capture.release()
    #     open_cv.destroyAllWindows()

    # def __apply(self, grayed, index, p):
    #     #print(p) # self.data

    #     #coordinates= self._coordinates(p)
    #     #print(coordinates)
    #     #print(type(coordinates))

    #     #print(grayed, grayed.shape) # shape= (?, ?) ?는 위에서 확인한 capture의 값과 같다.
    #     #roi_gray= open_cv.circle(grayed, (p['x'], p['y']), p['r'])
    #     roi_gray= grayed[p['y']:p['y']+p['r'], p['x']:p['x']+p['r']]
    #     #print(roi_gray, roi_gray.shape) # shape= (20,20) 왜?
    #     laplacian= open_cv.Laplacian(roi_gray, open_cv.CV_64F)
    #     #print(laplacian, laplacian.shape) # shape= (20, 20)

    #     status= np.mean(np.abs(laplacian * self.mask[index]))< MotionDetector.LAPLACIAN

    #     return status

    # @staticmethod
    # def _coordinates(p):
    #     return np.array(p)#["coordinates"])

    # @staticmethod
    # def same_status(coordinates_status, index, status):
    #     return status== coordinates_status[index]

    # @staticmethod
    # def status_changed(coordinates_status, index, status):
    #     return status!= coordinates_status[index]


