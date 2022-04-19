import cv2 as open_cv
import numpy as np
import json
from colors import COLOR_WHITE
from drawing_utils import draw_contours

class CoordinatesGenerator:
    KEY_RESET= ord('r')
    KEY_QUIT= ord('q')

    def __init__(self, image, output, color):
        self.caption= image
        '''
        output= data_file에 작성할 points
        '''
        self.output= output
        self.color= color
        self.image= open_cv.imread(image).copy()
        self.ids= 0
        self.coordinates= []
        self.data= {'data': []}

        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        # window 이름 설정 시 imshow할 창 이름과 틀리면 안 된다. 주의
        open_cv.setMouseCallback(self.caption, self.__mouse_click)
    
    def generate(self):
        '''
        key r 또는 R을 입력 시에 copy된 clone이 다시 img가 되면서
        while문과 함께 리셋이 되는 효과를 가져옵니다.
        '''
        while 1:
            open_cv.imshow(self.caption, self.image)
            key= open_cv.waitKey(0)& 0xFF
            json.dump(self.data, self.output, indent= 4)

            if key== CoordinatesGenerator.KEY_RESET:
                self.image= self.image.copy()

            elif key== CoordinatesGenerator.KEY_QUIT:
                break
        
        open_cv.destroyWindow(self.caption)

    '''
    마우스 클릭 시, 생성되는 좌표를 저장해놓고 그 위치에 원을 생성합니다.
    '''
    def __mouse_click(self, event, x, y, flags, params):
        if event== open_cv.EVENT_LBUTTONDOWN:

            '''
            클릭 시 좌표를 저장
            '''
            radius= 15
            self.coordinates.append((x, y, radius))
            self.__handle_done()

        open_cv.imshow(self.caption, self.image)

    def __handle_done(self):
        open_cv.circle(self.image, (self.coordinates[0][0], self.coordinates[0][1]), self.coordinates[0][2], self.color, 1)
        open_cv.imshow(self.caption, self.image)

        new_points= {'id': self.ids, 
                     'coordinates': [self.coordinates[0][0], self.coordinates[0][1], self.coordinates[0][2]],
                    }
        self.data['data'].append(new_points)

        '''
        외곽선 그리기

        외곽선 계층 정보는 ndarray 데이터로 저장합니다.
        '''
        coordinates= np.array([[self.coordinates[0][0], self.coordinates[0][1]]])
        #print(coordinates)
        draw_contours(self.image, coordinates, str(self.ids+ 1), COLOR_WHITE)

        '''
        클릭했던 좌표 정보 삭제
        '''
        self.coordinates.pop()

        '''
        클릭한 원 개수 추가
        '''
        self.ids+= 1

        