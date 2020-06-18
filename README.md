# ITS (Intelligent Traffic System) là gì?
[![Build Status](/images/passing.svg/)](/)

ITS là hệ thống phân tích giao thông bao gồm các thành phần:
|  | Tên thành phần | Link |
| ------ | ------ | ------ |
| 1 | Phân tích lưu lượng giao thông | here! |
| 2 | Nhận diện tai nạn giao thông | [link!](https://github.com/xinchaothegioi31415/Accident-Regconition-ML) |
| 3 | Công nghệ phát hiện vượt đèn đỏ | [link!](https://github.com/xinchaothegioi31415/Red-Light-Detection) |

>Hệ thống sử dụng công nghệ Machine Learning thông qua thư viện mã nguồn mở [Darkflow](https://github.com/thtrieu/darkflow) để huấn luyện cho máy tính.
>Ngoài ra, hệ thống còn sử dụng thư viện mã nguồn mở OpenCV để phân tích hình ảnh.

# Phân tích lưu lượng giao thông
**"Phân tích lưu lượng giao thông"** là một phần nhỏ trong hệ thống ITS, sử dụng thư viện mã nguồn mở OpenCV (open-source library) là chủ yếu để phân tích hình ảnh và trả kết quả về CSDL Firebase.
> Phần phân tích này, chúng tôi có tham khảo phương pháp [tại đây!](https://github.com/creotiv/object_detection_projects/tree/master/opencv_traffic_capacity_counting)

![Image](/images/intro.png/ "Hệ thống phân tích lưu lượng giao thông")

# Dependencies
Python3, firebase, firebase-admin, pyrebase, matplotlib (3.1.2), opencv-python (4.1.1.26), numpy (1.16.3)

# Hướng dẫn cài đặt
### Tải Python 3.7.3
> Bạn có thể tải Python 3.7.3 tại **[trang chính thức!](https://www.python.org/downloads/release/python-373/)**
### Clone project
Trước tiên, bạn cần clone dự án thông qua các cách:
- Thông qua Git:
```sh
$ git clone https://github.com/xinchaothegioi31415/ITS-Traffic-Capacity-Analyzation.git
```
![Image](/images/image2.png/ "Image2")
- Hoặc tải xuống trực tiếp thông qua các cách sau:
![Image](/images/image1.png/ "Image1")
### Cài đặt
1. Truy cập thư mục của dự án vừa clone ở trên, nhập **"cmd"** để mở *Command Prompt*.
2. Nhập dòng lệnh sau để cài đặt các thư viện cần thiết:
```sh
$ pip install -r requirement.txt
```
![Image](/images/image3.png/ "Image3")
3. Hoặc cài đặt từng thư viện:
```sh
$ pip install firebase
$ pip install firebase-admin
$ pip install pyrebase
$ pip install matplotlib==3.1.2
$ pip install opencv-python==4.1.1.26
$ pip install numpy==1.16.3
```
### Build dự án
Sau khi cài đặt xong, bạn nhập vào **"cmd"** dòng lệnh sau để tiến hành chạy chương trình:
```sh
$ python main.py
```
![Image](/images/image4.png/ "Image4")

### Video hướng dẫn
[![VIDEO HƯỚNG DẪN](https://yt-embed.herokuapp.com/embed?v=GlTSvSGjCzc)](https://youtu.be/GlTSvSGjCzc "VIDEO HƯỚNG DẪN")
***
Xong rồi! Hell yeah! 😁
