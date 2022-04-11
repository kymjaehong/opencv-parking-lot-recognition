import cv2 as open_cv

'''
이미지 파일을 flags값에 따라 읽어 옵니다.
imread(file_name, flags)

default flags는 cv2.IMREAD_COLOR 입니다.
'''
img= open_cv.imread('seulgi.jpeg', open_cv.IMREAD_COLOR)

'''
이미지를 보는 함수입니다.
imshow(title, image)

title은 window 창의 Title로 str
image는 ndarray로 imread의 return 값입니다.
'''
open_cv.imshow('image', img)

'''
waitKey(0) 
키 입력을 무한히 기다립니다.
->
destroyAllwindows()
열려있는 윈도우 창을 종료합니다.
'''
open_cv.waitKey(0)
open_cv.destroyAllWindows()
