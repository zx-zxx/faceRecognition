import os
from flask import Flask, request, jsonify
import base64
import cv2
import insightface
import numpy as np
from sklearn import preprocessing # 用于数据预处理

app = Flask(__name__)
class FaceRecognition:
    def __init__(self, gpu_id=0, face_db='face_db', threshold=1.24, det_thresh=0.50, det_size=(640, 640)):
        """
        人脸识别工具类
        :param gpu_id: 正数为GPU的ID，负数为使用CPU
        :param face_db: 人脸库文件夹
        :param threshold: 人脸识别阈值
        :param det_thresh: 检测阈值
        :param det_size: 检测模型图片大小
        """
        self.gpu_id = gpu_id
        self.face_db = face_db # 设置人脸识别路径，即该文件夹下的face_db文件夹
        self.threshold = threshold
        self.det_thresh = det_thresh
        self.det_size = det_size

        # 加载人脸识别模型，当allowed_modules=['detection', 'recognition']时，只单纯检测和识别
        self.model = insightface.app.FaceAnalysis(root='~/.insightface',
                                                  allowed_modules=None,
                                                  providers=['CUDAExecutionProvider']) #初始化人脸识别模型
        self.model.prepare(ctx_id=self.gpu_id, det_thresh=self.det_thresh, det_size=self.det_size) # 准备模型
        # 人脸库的人脸特征
        self.faces_embedding = list()
        # 加载人脸库中的人脸
        self.load_faces(self.face_db)

    # 加载人脸库中的人脸
    def load_faces(self, face_db_path):
        # 检查是否有人脸库文件夹，没有则创建
        if not os.path.exists(face_db_path):
            os.makedirs(face_db_path)
        # 遍历人脸库文件夹中的所有文件
        for root, dirs, files in os.walk(face_db_path):
            for file in files:
                # root:当前目录名，file：当前文件名
                # os.path.join(root, file)：形成完整路径
                # np.uint8：解释为numpy数组，数据类型为为无符号8位整数，用于表示像素的灰度值
                # 参数1：读取彩色图片
                input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1) # 读取图片
                user_name = file.split(".")[0] # 获取用户名称
                face = self.model.get(input_image)[0] # 获取人脸信息
                # face.embedding：从人脸检测模型中提取特征向量
                # np.array(face.embedding)：将特征向量转为numpy数组
                # .reshape((1, -1))：设置形状为一行的二维数组，第一个维度是1，第二个维度取决于自动计算
                embedding = np.array(face.embedding).reshape((1, -1)) # 获取人脸特征
                embedding = preprocessing.normalize(embedding) # 归一化处理
                # 将人脸特征添加到人脸库中
                self.faces_embedding.append({
                    "user_name": user_name,
                    "feature": embedding
                })

    # 人脸比对
    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2) # 计算特征差异
        dist = np.sum(np.square(diff), 1) # 计算特征距离
        if dist < threshold:
            return True # 若距离小于阈值，返回成功
        else:
            return False

    # 注册人脸信息，一张图片里只能出现一张人脸
    def register(self, image, user_name):
        faces = self.model.get(image)
        if len(faces) != 1:
            return '图片检测不到人脸'
        # 判断人脸是否存在
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding) # 归一化处理，此时为当前待识别的人脸特征
        is_exits = False # 默认人脸信息不存在
        for com_face in self.faces_embedding: # 遍历人脸库的特征
            r = self.feature_compare(embedding, com_face["feature"], self.threshold) # 比较人脸特征
            if r:
                is_exits = True
        if is_exits:
            return '该用户已存在'
        # 符合注册条件保存图片，同时把特征添加到人脸特征库中
        cv2.imencode('.png', image)[1].tofile(os.path.join(self.face_db, '%s.png' % user_name))
        self.faces_embedding.append({
            "user_name": user_name,
            "feature": embedding
        })
        return "success"

    # 人脸识别
    def recognition(self, image):
        faces = self.model.get(image) # 检测图片中的人脸
        results = list() # 存储识别结果
        for face in faces: # 遍历每个人脸
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1)) # 获取人脸特征
            embedding = preprocessing.normalize(embedding) # 归一化处理
            user_name = "unknown" # 默认识别结果为未知
            for com_face in self.faces_embedding:
                # 比较人脸特征
                r = self.feature_compare(embedding, com_face["feature"], self.threshold)
                if r:
                    user_name = com_face["user_name"] # 更新识别结果
            results.append(user_name) # 将识别结果添加到列表中
        return results # 返回识别结果
    
    # 检测人脸
    # def detect(self, image, names):
    #     faces = self.model.get(image) # 检测图片中的人脸
    #     results = list()
    #     imgs = self.model.draw_on(image, faces, names)
    #     for face in faces:
    #         result = dict() # 存储单个人脸的检测结果
    #         # 获取人脸属性
    #         result["bbox"] = np.array(face.bbox).astype(np.int32).tolist() # 获取人脸框坐标
    #         result["kps"] = np.array(face.kps).astype(np.int32).tolist() # 获取人脸五个关键点
    #         result["landmark_3d_68"] = np.array(face.landmark_3d_68).astype(np.int32).tolist() # 获取人脸3D关键点
    #         result["landmark_2d_106"] = np.array(face.landmark_2d_106).astype(np.int32).tolist() # 获取人脸2D关键点
    #         result["pose"] = np.array(face.pose).astype(np.int32).tolist() # 获取人脸姿态
    #         result["age"] = face.age
    #         gender = '男'
    #         if face.gender == 0:
    #             gender = '女'
    #         result["gender"] = gender
    #         # 开始人脸识别
    #         embedding = np.array(face.embedding).reshape((1, -1))
    #         embedding = preprocessing.normalize(embedding)
    #         result["embedding"] = embedding # 存储人脸特征
    #         results.append(result)
    #     return results, imgs

@app.route("/register", methods=["POST"])
def register():
    # 获取POST请求中的Base64图像数据
    image_data = request.json.get('image')

    # 将Base64图像数据解码为numpy数组
    image_np = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR) # 输入注册图片
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    face_recognition = FaceRecognition()  # 初始化人脸识别工具
    # 人脸注册
    result = face_recognition.register(img, user_name='driver1')
    # 构造JSON数据
    json_data = {
        "function": 'face_register',
        "results": result
    }
    # print(json_data)
    return jsonify(json_data)

@app.route("/login", methods=["POST"])
def login():
    # 获取POST请求中的Base64图像数据
    image_data = request.json.get('image')

    # 将Base64图像数据解码为numpy数组
    image_np = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR) # 输入登录图片
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    face_recognition = FaceRecognition()  # 初始化人脸识别工具
    # 人脸识别
    result = face_recognition.recognition(img)
    json_data = {
        "function": 'face_recognition',
        "results": result
    }
    # print(json_data)
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port=5000)