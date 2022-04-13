import cv2 as open_cv

path= r'seulgi.jpeg'

'''
마우스 클릭 시, 생성되는 좌표를 저장해놓고 그 위치에 원을 생성합니다.
'''
refPt= []
def mouse_click(event, x, y, flags, params):
    global refPt
    if event== open_cv.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        radius= 20
        color= (255, 0, 0)
        thickness= 2
        open_cv.circle(img, refPt[0], radius, color, thickness)
        open_cv.imshow('image', img)

img= open_cv.imread(path)

'''
key r 또는 R을 입력 시에 copy된 clone이 다시 img가 되면서
while문과 함께 리셋이 되는 효과를 가져옵니다.
'''
clone= img.copy()
open_cv.namedWindow('image')
open_cv.setMouseCallback('image', mouse_click)

while 1:
    open_cv.imshow('image', img)
    key= open_cv.waitKey(1)& 0xFF

    if key== ord('r'):
        img= clone.copy()

    elif key== ord('q'):
        break

open_cv.destroyAllWindows()

