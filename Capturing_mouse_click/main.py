import argparse
import cv2 as open_cv

refPt= []
cropping= False

'''
EVENT_LBUTTONDOWN-> EVENT_LBUTTONUP
좌표 (x, y) 생성, refPt에 저장

cropping= False (클릭 x 상태)
        = True (클릭 상태)
'''
def click_and_cropping(event, x, y, flags, params):
    global refPt, cropping

    if event== open_cv.EVENT_LBUTTONDOWN:
        refPt= [(x, y)]
        cropping= True

    elif event== open_cv.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping= False

        open_cv.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        open_cv.imshow('image', image)

'''
명령 인자를 파씽해준다.
사용법 작성 및 예외 처리를 쉽게 할 수 있다.

터미널에서 파일 실행을 할 때, 어떤 파일을 사용할 지 등 한 번에 작성할 수 있다.
'''
arg= argparse.ArgumentParser()
arg.add_argument('-i', '--image', required= True, help= 'Path to the image')
args= vars(arg.parse_args())

'''
파씽한 이미지 파일을 imread로 읽어오기
copy한 clone은 cropping된 이미지를 보여주기 위한 변수
setMouseCallback 사용을 위해서 namedWindow로 윈도우 창 이름을 지정해준 뒤에
마우스 이벤트 처리 함수를 실행합니다. 
'''
image= open_cv.imread(args['image'])
clone= image.copy()
open_cv.namedWindow('image')
open_cv.setMouseCallback('image', click_and_cropping)

'''
& 0xFF의 의미
8비트 이진법을 사용한다는 의미입니다.

255미만의 정수만 입력 받을 수 있습니다.
그리고 R과 r을 같은 key로 받을 수 있게 됩니다.
'''
while 1:
    open_cv.imshow('image', image)
    key= open_cv.waitKey(1)& 0xFF

    if key== ord('r'):
        image= clone.copy()

    elif key== ord('c'):
        break

'''
Region of interest -> [y:y+h, x:x+w]
아까 copy한 clone의 영역을 축소하여 roi로 저장합니다.

마우스의 위치가 (x, y)로 저장되기에 조건에 맞춰 범위를 지정해줘야 합니다.
'''
if len(refPt)== 2:
    roi= clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    #roi= clone[refPt[0][0]:refPt[1][0], refPt[0][1]:refPt[1][1]]   # 조건에 어긋날 시 에러 발생
    open_cv.imshow('ROI', roi)
    open_cv.waitKey(0)

open_cv.destroyAllWindows()