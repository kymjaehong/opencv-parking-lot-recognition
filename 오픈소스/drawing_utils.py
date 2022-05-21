import cv2 as open_cv
from colors import COLOR_RED


def draw_contours(image,
                  coordinates,
                  label,
                  font_color,
                  border_color= COLOR_RED,
                  line_thickness= 1,
                  font= open_cv.FONT_HERSHEY_SIMPLEX,
                  font_scale= 0.5):
    '''
    검출한 외곽선을 그려주는 함수
    '''
    open_cv.drawContours(image,    # 원본 이미지
                     [coordinates],    # contours 정보
                     contourIdx= -1,    # contours list type에서 몇 번째 contours line을 그릴 것인지, -1은 전체
                     color= border_color,   # contours line color
                     thickness= 2,  # contours line의 두께, 음수면 contours line의 내부를 채워준다.
                     lineType= open_cv.LINE_8)
    '''
    모멘트의 종류는 3가지로 공간, 중심, 평준화된 중심 모멘트가 있습니다.
    cv2.moments 함수는 이미지 모멘트를 계산하고 이를 사전형 자료에 담아 리턴합니다.
    총 24개의 값을 가지고 있습니다.
    '''
    moments= open_cv.moments(coordinates)

    '''
    무게 중심의 x 좌표, y 좌표 (변치 않음)

    x 좌표= int(moments['m10']/ moments['m00'])
    y 좌표= int(moments['m01']/ moments['m00'])
    '''
    center= (int(moments['m10']/ moments['m00'])- 3,
             int(moments['m01']/ moments['m00'])+ 3)

    '''
    text(내용)= label을 사각형 왼쪽 아래 org(좌표)= center에 
    폰트(fonstFace), 폰트스케일(FontScale), color로 문자를 출력한다.
    '''
    open_cv.putText(image,
                label,
                center,
                font,
                font_scale,
                font_color,
                line_thickness,
                open_cv.LINE_AA)
