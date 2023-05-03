from flask import Flask, render_template, request, jsonify
import os
import cv2
import pandas as pd
import glob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open_image', methods=['POST'])
def open_image():
    image_path = request.form.get('image_path')
    img = cv2.imread(image_path)
    img = cv2.resize(img, (960, 540))

    rectangle_points = []

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
            rectangle_points.append((x, y))

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', on_mouse)

    while True:
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF

        if key == 13 or len(rectangle_points) == 4:
            break

    cv2.destroyAllWindows()
    return jsonify({'rectangle_points': rectangle_points})

# Step 1
def get_scale_factor(image_path):
    window_name = 'Select rectangle corners'
    points = []

    def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow(window_name, img)

    img = cv2.imread(image_path)
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_circle)

    while True:
        cv2.imshow(window_name, img)
        if cv2.waitKey(20) & 0xFF == 27 or len(points) == 4:
            break

    cv2.destroyAllWindows()

    real_distance = float(input("Enter the real distance for one side of the rectangle: "))
    pixel_distance = ((points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2) ** 0.5
    scale_factor = real_distance / pixel_distance

    return scale_factor

# Step 2
def read_csv_files(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            data = pd.read_csv(filepath, skiprows=2, usecols=["coords", "x", "y"])
            all_data.append(data)

    return pd.concat(all_data)

# Step 3

def is_inside_rectangle(point, rectangle_points):
    x, y = point
    x1, y1, x2, y2, x3, y3, x4, y4 = rectangle_points

    # Compute vectors
    v0 = (x4 - x1, y4 - y1)
    v1 = (x2 - x1, y2 - y1)
    v2 = (x3 - x2, y3 - y2)

    # Compute dot products
    dot00 = v0[0] * v0[0] + v0[1] * v0[1]
    dot01 = v0[0] * v1[0] + v0[1] * v1[1]
    dot02 = v0[0] * v2[0] + v0[1] * v2[1]
    dot11 = v1[0] * v1[0] + v1[1] * v1[1]
    dot12 = v1[0] * v2[0] + v1[1] * v2[1]

    # Compute barycentric coordinates
    inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    # Check if point is in rectangle
    return (u >= 0) and (v >= 0) and (u + v <= 1)

def calculate_movements(data, scale_factor, rectangle_points):
    movements = 0
    prev_inside = is_inside_rectangle((data.iloc[0]['x'], data.iloc[0]['y']), rectangle_points)

    for i in range(1, len(data)):
        point = (data.iloc[i]['x'], data.iloc[i]['y'])
        inside = is_inside_rectangle(point, rectangle_points)

        if inside != prev_inside:
            movements += 1

        prev_inside = inside

    return movements

# Step 4
def calculate_time_inside_rectangle(data, rectangle_points):
    time_inside = 0

    for i in range(len(data)):
        point = (data.iloc[i]['x'], data.iloc[i]['y'])
        if is_inside_rectangle(point, rectangle_points):
            time_inside += 1

    return time_inside / 30  # 每30個id為1秒

@app.route('/process', methods=['POST'])
def process():
    image_path = request.form.get('image_path')
    folder_path = request.form.get('folder_path')
    rectangle_points = request.form.get('rectangle_points', type=str).split(',')
    scale_factor = get_scale_factor(image_path)
    data = read_csv_files(folder_path)

    # Step 3
    movements = calculate_movements(data, scale_factor, rectangle_points)

    # Step 4
    time_inside = calculate_time_inside_rectangle(data, rectangle_points)

    return jsonify({'movements': movements, 'time_inside': time_inside})

if __name__ == '__main__':
    app.run(debug=True)
