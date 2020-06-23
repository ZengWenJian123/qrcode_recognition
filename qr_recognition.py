import cv2
from pyzbar import pyzbar
#二维码动态识别
camera=cv2.VideoCapture(0)
camera.set(3,1280) #设置分辨率
camera.set(4,768)
while True:
    (grabbed,frame)=camera.read()
    #获取画面中心点
    h1,w1= frame.shape[0],frame.shape[1]

    # 纠正畸变（这里把相机标定的代码去除了，各位自行标定吧）
    dst = frame

    # 扫描二维码
    text = pyzbar.decode(dst)
    for texts in text:
        textdate = texts.data.decode('utf-8')
        print(textdate)
        (x, y, w, h) = texts.rect#获取二维码的外接矩形顶点坐标
        print('识别内容:'+textdate)

        # 二维码中心坐标
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        cv2.circle(dst, (cx, cy), 2, (0, 255, 0), 8)  # 做出中心坐标
        print('中间点坐标：',cx,cy)
        coordinate=(cx,cy)
        #在画面左上角写出二维码中心位置
        cv2.putText(dst,'QRcode_location'+str(coordinate),(20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #画出画面中心与二维码中心的连接线
        cv2.line(dst, (cx,cy),(int(w1/2),int(h1/2)), (255, 0, 0), 2)
        #cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 做出外接矩形
        #二维码最小矩形
        cv2.line(dst, texts.polygon[0], texts.polygon[1], (255, 0, 0), 2)
        cv2.line(dst, texts.polygon[1], texts.polygon[2], (255, 0, 0), 2)
        cv2.line(dst, texts.polygon[2], texts.polygon[3], (255, 0, 0), 2)
        cv2.line(dst, texts.polygon[3], texts.polygon[0], (255, 0, 0), 2)
        #写出扫描内容
        txt = '(' + texts.type + ')  ' + textdate
        cv2.putText(dst, txt, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 50, 255), 2)


    cv2.imshow('dst',dst)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q保存一张图片
        cv2.imwrite("./frame.jpg", frame)
        break

camera.release()
cv2.destroyAllWindows()