import cv2 as open_cv
import numpy as np

from colors import COLOR_WHITE
from drawing_utils import draw_contours


class CoordinatesGenerator:
    KEY_RESET= ord('r')
    KEY_QUIT= ord('q')

    def __init__(self, image, output, color):
        self.caption= image
        self.output= output
        self.color= color

        '''
        이미지 파일을 flags값에 따라 읽어 옵니다.
        imread(file_name, flags)

        default flags는 cv2.IMREAD_COLOR 입니다.
        '''
        self.image= open_cv.imread(image).copy()
        self.click_count= 0
        self.ids= 0
        self.coordinates= []

        '''
        창 관리
        namedWindow(window_name, flags)
        window_name이라는 이름을 갖는 창을 창 옵션(flags)에 맞게 생성해줍니다.
        '''
        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        '''
        Mouse Event를 확인하고 Callback을 호출하는 함수입니다.
        setMouseCallback(window_name, callback, param)

        callback은 callback 함수를 정의해서 사용합니다.
        여기에는 (event, x, y, flags, param)이 전달됩니다.

        param은 callback 함수에서 전달되는 data
        '''
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
            while 1:
                '''
                이미지를 보는 함수입니다.
                imshow(title, image)

                title은 window 창의 Title로 str
                image는 ndarray로 imread의 return 값입니다.
                '''
                open_cv.imshow(self.caption, self.image)
                '''
                waitKey는 키 입력을 기다리는 함수입니다.
                입력된 키는 아스키 값에 의거하여 확인됩니다.
                아무것도 입력되지 않으면 -1
                함수 안에 0을 입력하면 무한 대기를 의미합니다.
                '''
                key= open_cv.waitKey(0)

                if key== CoordinatesGenerator.KEY_RESET:
                    self.image= self.image.copy()

                elif key== CoordinatesGenerator.KEY_QUIT:
                    break
            
            '''
            해당 창 이름의 window 창을 닫습니다.
            destroyWindow
            '''
            open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params): # on_mouse라는 함수명을 사용해도 괜찮을 것 같다.
            '''
            EVENT_LBUTTONDOWN은 마우스 왼쪽 버튼 클릭 시를 의미합니다.
            '''
            if event== open_cv.EVENT_LBUTTONDOWN:
                self.coordinates.append((x,y))
                self.click_count+= 1

                if self.click_count>= 4:
                    self.__handle_done()

                elif self.click_count> 1:
                    self.__handle_click_progress()

            open_cv.imshow(self.caption, self.image)

    '''
    직선 그리기
    cv2.line(image, start, end, color, thickness, lineType)

    image는 imread로 읽어온 파일
    start, end는 좌표
    color는 BGR 순서로 
    thickness는 선의 두께로 pixel, default는 1
    lineType은 cv2.LINE_로 시작하는 값
    '''
    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255,0,0), 1)

    def __handle_done(self):
        open_cv.line(self.image,
                    self.coordinates[2],
                    self.coordinates[3],
                    self.color,
                    1)
        open_cv.line(self.image,
                    self.coordinates[3],
                    self.coordinates[0],
                    self.color,
                    1)      

        self.click_count= 0

        coordinates= np.array(self.coordinates)

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                            "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                            "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                            "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                            "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")
        
        '''
        open_cv에서는 GBR이므로 coordinates는 default로 설정된 COLOR_RED는 BLUE로 나타난다.
        '''
        draw_contours(self.image, coordinates, str(self.ids+ 1), COLOR_WHITE)

        for i in range(4):
            self.coordinates.pop()

        self.ids+= 1
