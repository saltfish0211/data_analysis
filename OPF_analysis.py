# coding: utf-8
#v1.0

import cv2
import os
import glob
import pandas as pd
import numpy as np

# 鼠標點擊事件回調函數
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))

# 計算兩點之間的距離
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 判斷點是否在矩形內
def is_inside_rect(p, rect_points):
    a, b, c, d = rect_points
    v0 = np.array(c) - np.array(a)
    v1 = np.array(b) - np.array(a)
    v2 = np.array(p) - np.array(a)

    u = np.dot(v2, v0) / np.dot(v0, v0)
    v = np.dot(v2, v1) / np.dot(v1, v1)

    return (0 <= u <= 1) and (0 <= v <= 1)

# 主程式
if __name__ == "__main__":
    # 1. 讀取圖片並選擇矩形四個頂點
    image_path = 'path/to/image/file.jpg'
    image = cv2.imread(image_path)
    clicked_points = []

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse_click)

    while len(clicked_points) < 4:
        cv2.imshow('image', image)
        cv2.waitKey(50)

    cv2.destroyAllWindows()

    # 輸入矩形一邊的真實距離
    real_distance = float(input("請輸入矩形一邊的真實距離（單位：公尺）："))

    # 計算比例尺
    scale = real_distance / distance(clicked_points[0], clicked_points[1])

    # 2. 讀取 CSV 文件
    data_path = 'path/to/csv/folder'
    csv_files = glob.glob(os.path.join(data_path, "*.csv"))
    data_list = []

    for f in csv_files:
        data_list.append(pd.read_csv(f, header=2, usecols=["coords", "x", "y"]))

    data = pd.concat(data_list)

    # 3. 計算移動距離和進出次數
    move_distance = 0
    enter_count = 0
    exit_count = 0
    prev_inside = is_inside_rect(data.iloc[0][['x', 'y']].to_numpy(), clicked_points)

    for i in range(1, len(data)):
        prev_point = data.iloc[i - 1][['x', 'y']].to_numpy()
        curr_point = data.iloc[i][['x', 'y']].to_numpy()
        move_distance += distance(prev_point, curr_point) * scale

        curr_inside = is_inside_rect(curr_point, clicked_points)
        if not prev_inside and curr_inside:
            enter_count += 1
        elif prev_inside and not curr_inside:
            exit_count += 1

        prev_inside = enter_count
    # 4. 計算矩形內的停留時間
    time_inside_rect = 0
    ids_inside_rect = 0

    for i in range(1, len(data)):
        curr_point = data.iloc[i][['x', 'y']].to_numpy()

        if is_inside_rect(curr_point, clicked_points):
            ids_inside_rect += 1

    time_inside_rect = ids_inside_rect / 30

# 輸出結果
print(f"移動總距離：{move_distance:.2f} 公尺")
print(f"進入矩形次數：{enter_count} 次")
print(f"退出矩形次數：{exit_count} 次")
print(f"矩形內的停留時間：{time_inside_rect:.2f} 秒")

