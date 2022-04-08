import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE
#from matplotlib import pyplot as plt


class MotionDetector:
    LAPLACIAN= 1.4
    DETECT_DELAY= 1

    def __init__(self, video, coordinates, start_frame):
        self.video= video
        self.coordinates_data= coordinates
        self.start_frame= start_frame
        self.contours= []
        self.bounds= []
        self.mask= []

    def detect_motion(self):
        '''
        VideoCapture(filename)
        비디오 파일 읽기

        메서드
        .set(propid, value)
        동영상 속성 설정
        '''
        capture= open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)  # 프레임 재생 시간을 설정하였다. 

        '''
        logging.debug(msg, *args, **kwargs)
        루트 로거에 수준 에러 발생 시 DEBUG 메세지를 로그합니다.
        
        msg는 메세지 포맷 문자열
        args는 문자열 포매팅 연산자를 사용하여 msg에 병합되는 인자
        kwargs에서 검사되는 3개의 인자가 있습니다.
            exc_info : 
            stack_info : 
            extra : 
        '''
        coordinates_data= self.coordinates_data
        '''
        4개의 좌표 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]가 1개의 coordinates_data입니다.
        '''
        #print(coordinates_data)
        logging.debug("coordinates data: %s", coordinates_data)
        #print(logging.debug("coordinates data: %s", coordinates_data)) 에러 발생을 하지 않으면 None

        for p in coordinates_data:
            coordinates= self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            '''
            boundingRect()
            주어진 점을 감싸는 최소 크기 바운딩 박스를 반환합니다.
            x, y, w, h 반환
            '''
            rect= open_cv.boundingRect(coordinates)
            '''
            1개의 coordinates_data에서 4개의 x, y좌표 중 최소 값으로 rect를 (min_x, min_y, width, height)가 반환
            '''
            #print(rect)
            logging.debug("rect: %s", rect)

            new_coordinates= coordinates.copy()
            new_coordinates[:, 0]= coordinates[:, 0]- rect[0]
            new_coordinates[:, 1]= coordinates[:, 1]- rect[1]
            '''
            [[new_coordinates의 x 좌표- rect의 min_x, new_coordinates의 y 좌표- rect의 min_y]
            ...좌표 4개니까 4개 반환]
            '''
            #print(new_coordinates)
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)
            #print(self.contours)    # coordinates_data 저장
            #print(self.bounds)  # rect 저장

            mask= open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask= mask== 255
            self.mask.append(mask)
            #print(self.mask)    # drawContour로 생성된 array에서 값이 255면 True 아니면 False 반환
            logging.debug("mask: %s", self.mask)

        statuses= [False] * len(coordinates_data)
        times= [None] * len(coordinates_data)

        '''
        isOpened()
        동영상 파일 열기 성공 여부 확인
        '''
        while capture.isOpened():
            result, frame= capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))
            
            '''
            GaussianBlur(src, ksize, sigma)
            영상에 블러링(가우시안 필터) 적용
            가까운 픽셀은 큰 가중치를, 멀리있는 픽셀은 작은 가중치를 사용하여 평균을 계산합니다.

            ksize는 커널 사이즈입니다. (0, 0)으로 입력시 sigma에 의해서 커널 사이즈가 자동 설정됩니다.
            sigma가 1, 2, 3 커질수록 사진은 흐릿해집니다.
            '''
            blurred= open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            '''
            cvtColor(src, code)
            색상 변환

            src는 입력 이미지를 imread를 읽어온 array
            code는 open_cv의 COLOR_ 메서드
            '''
            grayed= open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame= frame.copy()
            logging.debug("new_frame: %s", new_frame)

            '''
            .get(propid)
            동영상의 속성을 반환
            '''
            position_in_seconds= capture.get(open_cv.CAP_PROP_POS_MSEC)/ 1000.0 # 프레임 재생 시간을 ms로 반환
            #print(position_in_seconds)

            for index, c in enumerate(coordinates_data):
                status= self.__apply(grayed, index, c)
                #print(times[index])

                '''
                차가 들어와 있을 때 

                times[index] is not None인데 None으로 바꾸고 continue했기에
                조건 차가 들어왔을 때로 이동 
                '''
                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index]= None
                    continue
                
                '''
                차가 나갔을 때

                DETECT_DELAY를 기준으로 차가 있는지 없는지 판단한다.
                기준 이상이면 True
                '''
                if times[index] is not None and self.status_changed(statuses, index, status):
                    #print(position_in_seconds- times[index])
                    if position_in_seconds- times[index]>= MotionDetector.DETECT_DELAY:
                        '''
                        차가 나가면, 없을 때 True
                        차가 들어오면 False
                        '''
                        statuses[index]= status
                        #print(statuses[index])
                        times[index]= None
                    continue
                
                '''
                차가 들어왔을 때

                times[index]= None-> 현재 시간 기록
                '''
                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index]= position_in_seconds
                    #print(times[index])    # 차가 들어온 시간

            for index, p in enumerate(coordinates_data):
                coordinates= self._coordinates(p)
                
                '''
                open_cv에서는 GBR이므로 차가 없을 때는 True이므로 GREEN
                                     차가 들어왔을 때는 False이므로 RED
                '''
                color= COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            open_cv.imshow(str(self.video), new_frame)
            k= open_cv.waitKey(1)
            if k== ord("q"):
                break
        '''
        release()
        동영상 파일을 닫고 메모리 해제

        destroyAllWindows()
        열린 창 닫기
        '''
        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates= self._coordinates(p)
        #print(coordinates)
        logging.debug("points: %s", coordinates)

        rect= self.bounds[index]
        #print(rect)
        logging.debug("rect: %s", rect)

        '''
        grayed[y:(y+height), x:(x+width)]
        '''
        roi_gray= grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian= open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0]= coordinates[:, 0] - rect[0]
        coordinates[:, 1]= coordinates[:, 1] - rect[1]

        '''
        LAPLACIAN 기준으로 T/F 반환 -> status

        차가 들어오면 False로 반환
        '''
        status= np.mean(np.abs(laplacian * self.mask[index]))< MotionDetector.LAPLACIAN
        #plt.imshow(np.abs(laplacian * self.mask[index]))
        #plt.show()
        logging.debug("status: %s", status)

        return status

    '''
    yaml 파일이 [dictionary로 id... coordinates로 저장되어있는데 coordinates만 가져온다.]
    '''
    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status== coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status!= coordinates_status[index]


class CaptureReadError(Exception):
    pass
