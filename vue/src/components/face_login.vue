<template>
  <div class="body">
    <!-- 主要容器，包含注册和登录表单 -->
    <div class="main-box">
      <!-- 注册表单容器 -->
      <div :class="['container', 'container-register', { 'is-txl': isLogin }]">
        <!-- 表单开始 -->
        <form>
          <p>{{text}}</p>
          <div v-if="!showLoadingImage1">
            <video ref="video1" width="640" height="480" autoplay></video>
          </div>
          <div v-else class="loading-container">
            <img src="../assets/R.gif" alt="等待人脸识别" class="loading-image"/>
          </div>
          <button @click="captureRegisterImage">{{ regButtonText }}</button>
          <canvas ref="canvas1" width="640" height="480" style="display:none;"></canvas>
        </form>
      </div>
      <!-- 登录表单容器 -->
      <div :class="['container', 'container-login', { 'is-txl is-z200': isLogin }]">
        <!-- 表单开始 -->
        <form>
          <p>{{text}}</p>
          <div v-if="!showLoadingImage2">
            <video ref="video2" width="640" height="480" autoplay></video>
          </div>
          <div v-else class="loading-container">
            <img src="../assets/R.gif" alt="等待人脸识别" class="loading-image"/>
          </div>
          <button @click="captureLoginImage">{{ loginButtonText }}</button>
          <canvas ref="canvas2" width="640" height="480" style="display:none;"></canvas>
        </form>
      </div>
      <!-- 切换按钮容器 -->
      <div :class="['switch', { 'login': isLogin }]">
        <!-- 切换按钮的圆形装饰 -->
        <div class="switch__circle"></div>
        <div class="switch__circle switch__circle_top"></div>
        <!-- 切换按钮文本容器 -->
        <div class="switch__container">
          <h2>{{ isLogin ? '您好 !' : '欢迎回来 !' }}</h2>
          <p>
            {{
              isLogin
                ? '如果您还没有账号，请点击下方立即注册按钮进行账号注册'
                : '如果您已经注册过账号，请点击下方立即登录按钮进行登录'
            }}
          </p>
          <!-- 切换注册和登录状态的按钮 -->
          <div class="form__button" @click="isLogin = !isLogin">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'log-in',
  data() {
    return {
      text: "请将脸部正对摄像头并填充满取景框",
      regButtonText: "捕获图像并注册",
      loginButtonText: "捕获图像并登录",
      count: 0,
      isLogin: true,
      showLoadingImage1: false, // 等待图片显示状态
      showLoadingImage2: false,
      videoStreamForRegister: null,
      videoStreamForLogin: null,
    }
  },
  mounted() {
    // 循环请求识别接口
    this.startVideoStreamForRegister();
    this.startVideoStreamForLogin();
  },
  methods: {
    // 注册逻辑
    startVideoStreamForRegister() {
      // 请求用户媒体设备，获取视频流
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.videoStreamForRegister = stream;
          this.$refs.video1.srcObject = stream;
        })
        .catch(error => {
          console.error('获取视频流失败:', error);
        });
    },
    captureRegisterImage() {
      this.text = "人脸识别中..."
      const canvas = this.$refs.canvas1;
      const context = canvas.getContext('2d');
      const video = this.$refs.video1;
      // 显示等待人脸识别图片
      this.showLoadingImage1 = true;

      // 在画布上绘制视频当前帧
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // 停止视频流
      this.videoStreamForRegister.getTracks().forEach(track => {
        track.stop();
      });

      // 获取图像数据并转换为Base64编码
      const imageBase64 = canvas.toDataURL('image/jpeg').split(',')[1];

      // 发送图像数据到服务器
      this.sendRegisterImageToServer(imageBase64);
    },
    sendRegisterImageToServer(imageBase64) {
      const apiUrl = 'http://localhost:5000/register'; // 服务器API地址
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageBase64 })
      })
      .then(response => response.json())
      .then(data => {
        this.text = "人脸识别完成";
        // 识别完成后隐藏等待图片
        this.showLoadingImage1 = false;
        if (data.results == 'success') {
          // 注册成功
          this.text += '，注册成功！请登录';
          this.isLogin = !this.isLogin; // 切换到登录界面
        } else if (data.results == '该用户已存在') {
          this.text = '该用户已存在，请登录';
          this.isLogin = !this.isLogin; // 切换到登录界面
        }
        else {
          // 注册失败
          this.text += '，注册失败！';
          this.text += data.results;
          this.showLoadingImage1 = false;
          this.regButtonText = '重新捕获图像注册';
          this.startVideoStreamForRegister();
        }
        console.log('服务器响应:', data);
        // 处理服务器响应
      })
      .catch(error => {
        this.text += "发送请求时出错!";
        this.regButtonText = '重新捕获图像注册';
        this.startVideoStreamForRegister();
        console.error('发送请求时出错:', error);
      });
    },


    // 登录逻辑
    startVideoStreamForLogin() {
      // 请求用户媒体设备，获取视频流
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.videoStreamForLogin = stream;
          this.$refs.video2.srcObject = stream;
        })
        .catch(error => {
          console.error('获取视频流失败:', error);
        });
    },
    captureLoginImage() {
      this.text = "人脸识别中..."
      const canvas = this.$refs.canvas2;
      const context = canvas.getContext('2d');
      const video = this.$refs.video2;
      // 显示等待人脸识别图片
      this.showLoadingImage2 = true;

      // 在画布上绘制视频当前帧
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // 停止视频流
      this.videoStreamForLogin.getTracks().forEach(track => {
        track.stop();
      });

      // 获取图像数据并转换为Base64编码
      const imageBase64 = canvas.toDataURL('image/jpeg').split(',')[1];

      // 发送图像数据到服务器
      this.sendLoginImageToServer(imageBase64);
    },
    sendLoginImageToServer(imageBase64) {
      const apiUrl = 'http://localhost:5000/login'; // 服务器API地址
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageBase64 })
      })
      .then(response => response.json())
      .then(data => {
        this.text = "人脸识别完成";
        // 识别完成后隐藏等待图片
        this.showLoadingImage2 = false;
        if (data.results[0] != 'unknown') {
          // 登录成功
          this.text += '，登录成功！';
          // 进入到登录界面
          this.$router.push('/main');
        
        } else {
          // 登录失败
          this.text += '，登录失败！';  
          this.showLoadingImage2 = false;        
          this.loginButtonText = '重新捕获图像登录';
          this.startVideoStreamForLogin();         
        }
        console.log('服务器响应:', data);
        // 处理服务器响应
      })
      .catch(error => {
        this.text += "发送请求时出错!";
        this.loginButtonText = '重新捕获图像登录';
        this.startVideoStreamForLogin();
        console.error('发送请求时出错:', error);
      });
    }
  },

  beforeUnmount() {
    // 组件销毁前停止视频流
    if (this.videoStreamForRegister) {
      this.videoStreamForRegister.getTracks().forEach(track => {
        track.stop();
      });
    }
    if (this.videoStreamForLogin) {
      this.videoStreamForLogin.getTracks().forEach(track => {
        track.stop();
      });
    }
  },
}
</script>
  
<style scoped>
.body {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Montserrat", sans-serif;
  font-size: 12px;
  background-image: url("@/assets/background.jpg");
  color: #a0a5a8;
}

.main-box {
  position: relative;
  width: 1000px;
  min-width: 1000px;
  min-height: 600px;
  height: 600px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 1px 1px 100px 10px #ecf0f3;
  border-radius: 12px;
  overflow: hidden;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 0;
  width: 600px;
  height: 100%;
  padding: 25px;
  background-color: #ecf0f3;
  transition: all 1.25s;
}

form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  color: #a0a5a8;
}

.loading-container {
  width: 640px;
  height: 480px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.loading-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片铺满容器 */
}

.container-register {
  z-index: 100;
  left: calc(100% - 600px);
}

.container-login {
  left: calc(100% - 600px);
  z-index: 0;
}

.is-txl {
  left: 0;
  transition: 1.25s;
  transform-origin: right;
}

.is-z200 {
  z-index: 100;
  transition: 1.25s;
}

.switch {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 400px;
  padding: 50px;
  z-index: 200;
  transition: 1.25s;
  background-color: #ecf0f3;
  overflow: hidden;
  box-shadow: 4px 4px 10px #d1d9e6, -4px -4px 10px #f9f9f9;
  color: #a0a5a8;
}

.switch__circle {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background-color: #ecf0f3;
  box-shadow: inset 8px 8px 12px #d1d9e6, inset -8px -8px 12px #f9f9f9;
  bottom: -60%;
  left: -60%;
  transition: 1.25s;
}

.switch__circle_top {
  top: -30%;
  left: 60%;
  width: 300px;
  height: 300px;
}

.switch__container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: absolute;
  width: 400px;
  padding: 50px 55px;
  transition: 1.25s;
}
.switch__container h2 {
  font-size: 34px;
  font-weight: 700;
  line-height: 3;
  color: #181818;
}
.switch__container p {
  font-size: 14px;
  letter-spacing: 0.25px;
  text-align: center;
  line-height: 1.6;
}

.login {
  left: calc(100% - 500px);
}

.login .switch__circle {
  left: 0;
}

.form__button {
  width: 180px;
  height: 50px;
  border-radius: 25px;
  margin-top: 50px;
  text-align: center;
  line-height: 50px;
  font-size: 14px;
  letter-spacing: 2px;
  background-color: #4b70e2;
  color: #f9f9f9;
  cursor: pointer;
  box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #f9f9f9;
}

.form__button:hover {
  box-shadow: 2px 2px 3px 0 rgba(255, 255, 255, 50%),
  -2px -2px 3px 0 rgba(116, 125, 136, 50%),
  inset -2px -2px 3px 0 rgba(255, 255, 255, 20%),
  inset 2px 2px 3px 0 rgba(0, 0, 0, 30%);
}

button {
  width: 180px;
  height: 50px;
  border-radius: 25px;
  margin-top: 5px;
  text-align: center;
  line-height: 50px;
  font-size: 14px;
  letter-spacing: 2px;
  background-color: #4b70e2;
  color: #f9f9f9;
  cursor: pointer;
  box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #f9f9f9;
  border: 0px;  /*不知道为什么不加这句话，这个button会有边框 */
}

button:hover {
  box-shadow: 2px 2px 3px 0 rgba(255, 255, 255, 50%),
  -2px -2px 3px 0 rgba(116, 125, 136, 50%),
  inset -2px -2px 3px 0 rgba(255, 255, 255, 20%),
  inset 2px 2px 3px 0 rgba(0, 0, 0, 30%);
}

p {
  font-size: 16px;
}
</style>