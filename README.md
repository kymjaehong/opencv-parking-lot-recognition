# 주차장 내 주차 공간 인식
![](Parking_lot_circle/result_video.mov)

## 사용 방법
```
python3 main.py --image images/parking_lot_1.png --data data/coordinates.json --video videos/parking_lot_1.mp4 --start-frame 400
```
## 주차 공간 인식 방법
- 오픈 소스<br>
마우스 클릭 4번으로 사각형 영역을 그려 판독<br>

- 커스텀<br>
마우스 클릭 1번으로 원 영역을 그린 후, 원 안에 정사각형 영역을 판독

## 기본 예제
- 블로그를 통해서 기본 예제를 공부했습니다.<br>

[OpenCV 이미지 읽기](https://github.com/kymjaehong/parking_lot/tree/main/Image_imread_show)<br>
[OpenCV 마우스 이벤트 & 이미지 Cropping](https://github.com/kymjaehong/parking_lot/tree/main/Capturing_mouse_click)<br>
[OpenCV JSON & 마우스 이벤트 & 원 그리기](https://github.com/kymjaehong/Parking-lot/tree/main/Circle_mouse_click)<br>

- 오픈 소스를 통해서 영상에서 주차 공간을 확인하는 예제를 공부했습니다. 

<a href= 'https://github.com/olgarose/ParkingLot'><img src="https://img.shields.io/badge/Open Source-666666?style=flat&logo=github&logoColor=FFFFFF"/>

[오픈 소스 커스텀](https://github.com/kymjaehong/Parking-lot/tree/main/Parking_lot_circle)