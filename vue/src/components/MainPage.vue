<template>
<div class="whole-container">

  <!--标题部分-->
  <div class="title-box">
    <div class="flex-item">
      <img class="img-box1" v-bind:src="imgUrl"/>
    </div>
    <div class="flex-item">
      <img class="title-bgimg" v-bind:src="bgimgUrl">
      <p class="title">驾驶员监测系统</p>
    </div>
    <div class="flex-item">
      <img class="img-box1" v-bind:src="imgUrl"/>
    </div>
  </div><!--/标题部分-->

   <!--内容部分-->
  <div class="content-box">
    <!--酒精浓度、温度、湿度-->
    <div class="info-box">
      <!--酒精浓度-->
      <div class="info-item">
        <span class="line"></span>
        <div class="content">酒精浓度</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)"  color=#C6C4BE SIZE=3></HR>
        <div id="app1">  
          <gauge-chart></gauge-chart> <!-- 使用刚才创建的 GaugeChart 组件 -->  
        </div>  <!--可视化表-->
      </div><!--/酒精浓度-->

      <!--温度-->
      <div class="info-item">
        <span class="line"></span>
        <div class="content">温度</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)" color=#C6C4BE SIZE=3></HR>
        <div id="app2">  
          <temperature-gauge></temperature-gauge> <!-- 使用刚才创建的 GaugeChart 组件 -->  
        </div>  <!--可视化表-->
      </div><!--/温度-->

      <div class="info-item">
        <span class="line"></span>
        <div class="content">湿度</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)"  color=#C6C4BE SIZE=3></HR>
        <div id="app3">  
          <MunityLine></MunityLine>
        </div> 
      </div>
    </div>

    <!--实时监测-->
    <div class="monitor-box">
      <div class="video-container">
        <div class="indicator-container">
          <button class="indicator seatbelt-indicator" :class="{ blinking: isSeatbeltFastened }" :style="buttonStyle" ></button>
          <button class="indicator tired-indicator"  :class="{ blinking: isTiredDriving }" :style="buttonStyle"></button>
          <button class="indicator drink-indicator" :class="{ blinking: isDrinking }" :style="buttonStyle" ></button>
          <button class="indicator smoke-indicator"  :class="{ blinking: isSmoking }" :style="buttonStyle"></button>
          <button class="indicator phone-indicator" :class="{ blinking: isPhoning }" :style="buttonStyle"></button>   
        </div>
        <img class="monitor-video" v-bind:src="videoUrl"/>
      </div>
      <div class="monitor-title"> 
        <img class="monitor-img" v-bind:src="monitorimgUrl">
        <p class="title-content">--实时监测--</p>  
      </div>
    </div>

    <!--烟雾浓度、心率、血氧-->
    <div class="info-box">
      <!--烟雾浓度-->
      <div class="info-item">
        <span class="line"></span>
        <div class="content">烟雾浓度</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)"  color=#C6C4BE SIZE=3></HR>
        <div id="app4">  
          <smog-line></smog-line>
        </div>  
      </div>
      <!--心率-->
      <div class="info-item">
        <span class="line"></span>
        <div class="content">心率</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)"  color=#C6C4BE SIZE=3></HR>
        <div id="app5">  
          <HeartRate></HeartRate>
        </div> 
      </div>
      <!--血氧-->
      <div class="info-item">
        <span class="line"></span>
        <div class="content">血氧</div>
        <HR class="divline" style="FILTER: alpha(opacity=100,finishopacity=0,style=3)"  color=#C6C4BE SIZE=3></HR>
        <div id="app6">  
          <blood-oxyen></blood-oxyen>
        </div>
      </div>
    </div><!--/内容部分-->
  </div>
</div>
</template>

<script>
import axios from 'axios';
import GaugeChart from './GaugeChart.vue'; // 假设 GaugeChart.vue 在 components 目录下
import TemperatureGauge from './TemperatureGauge.vue' // 假设 TemperatureGauge.vue 位于 components 文件夹中 
import MunityLine from './MunityLine.vue';
import HeartRate from './HeartRate.vue';
import BloodOxyen from './BloodOxyen.vue';
import SmogLine from './SmogLine.vue';

export default { 
  components: {  
    GaugeChart,   
    TemperatureGauge, // 注册 TemperatureGauge 组件
    MunityLine,
    HeartRate,
    BloodOxyen,
    SmogLine,
  },  
  data(){
    return{
      imgUrl:require("@/assets/titleImg/标题图片.png"),
      bgimgUrl:require("@/assets/titleImg/大标题背景.png"),
      videoUrl: "https://ai.arcsoft.com.cn/resource/images/dmsMonitor/principle_03_1.png",//"http://192.168.31.98:5000/video", 
      monitorimgUrl:require("@/assets/titleImg/小标题.png"),

      luminance: '0.0',
      temperature: '0.0',
      alcoholVolumn: '0.0',
      smokeDensity: '0.0',
      heartRate: '0.0',
      bloodOxygen: '0.0',

      isSeatbeltFastened: false, // 从后端获取的布尔值(是否系安全带)
      isTiredDriving: false, // 从后端获取的布尔值(是否疲劳驾驶)
      isDrinking: false,// 从后端获取的布尔值(是否喝水)
      isSmoking: false, // 从后端获取的布尔值(是否抽烟)
      isPhoning: true, // 从后端获取的布尔值(是否玩手机)
    }
  },  
  computed: {
    buttonStyle() {
      return {
        '--indicator-off-color': '#bcafa',
        '--indicator-on-color': 'red'
      };
    }
  },
  /*获取数据的其他代码*/
  methods: {
    /* 获取硬件侧监测数据 */
    async fetchHardSideData() {
      try {
        const response = await axios.get("https://5b0b41d195.st1.iotda-app.cn-north-4.myhuaweicloud.com:443/v5/iot/2072e3f5512e489f85026b0af08af987/devices/662d16d371d845632a074f0c_esp8266test1/shadow",
        {
          headers: {
            "X-Auth-Token": localStorage.getItem('token')
          }
        })
        const properties = response.data.shadow[0].reported.properties;
        console.log(properties);
        localStorage.setItem("alcoholVolumn", properties.alcohol);
        localStorage.setItem("temperature", properties.temp);
        localStorage.setItem("luminance", properties.hum);
        localStorage.setItem("smokeDensity", properties.smoke);
        localStorage.setItem("heartRate", properties.rate);
        localStorage.setItem("bloodOxygen", properties.oxygen);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    // 获取AI侧数据
  //   async fetchDriverStatesData() {
  //     try {
  //       let response = await axios.get("http://192.168.31.98:5000/json")
  //       let response_seatbelt = await axios.get("http://192.168.31.98:5001")
  //       console.log(response)
  //       console.log(response_seatbelt)
  //       this.isSeatbeltFastened = response_seatbelt.data.seatbelt;
  //       this.isTiredDriving = response.data.tired;
  //       this.isDrinking = response.data.drink;
  //       this.isSmoking = response.data.smoke;
  //       this.isPhoning = response.data.phone;
  //       console.log("isSeatbeltFastened: " + this.isSeatbeltFastened);
  //       console.log("isTiredDriving: " + this.isTiredDriving);
  //       console.log("isDrinking: " + this.isDrinking);
  //       console.log("isSmoking: " + this.isSmoking);
  //       console.log("isPhoning: " + this.isPhoning);
  //     } catch (error) {
  //       console.error('Error fetching data:', error);
  //     }
  //   }
  // },
    mounted() {
      // localStorage中有：refreshTokenTimeout, token, expires_at, tokenExpiryTime
      localStorage.setItem("refreshTokenTimeout", null);
      async function fetchToken() {
        const response = await axios.post(('https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'), 
        {"auth":{
            "identity":{
                "methods":["password"],
                "password":{
                "user":{
                    "name":"ccnuiot",
                    "password":"ccnuiotxx1",
                    "domain":{
                    "name":"robb04"
                    }
                }
                }
            },
            "scope":{
                "project":{
                "name": "cn-north-4"
                }
            }}},
            {
            header: {
                "Content-Type": "application/json;charset=utf8",
                "Host": "iam.cn-north-4.myhuaweicloud.com"
            }
            })

        const token = response.headers.get('X-Subject-Token');
        const expiresAt = new Date(response.data.token.expires_at) // expireAt: Sun Dec 17 1995 03:24:00 GMT+0800 (中国标准时间)
      
        // 存储Token和expires_at过期时间
        localStorage.setItem("token", token);
        localStorage.setItem("expires_at", expiresAt.toISOString()) // expires_at: YYYYMMDDTHHMMSSZ
        // 获取Token过期时间
        localStorage.setItem("tokenExpiryTime", expiresAt.getTime()); // tokenExpiryTime: 1714225987524
        console.log(localStorage.getItem("token"));
      }

      function scheduleTokenRefresh() {
        // 清除现有的定时器
        if (localStorage.getItem("refreshTokenTimeout")) {
          clearTimeout(localStorage.getItem("refreshTokenTimeout"));
        }

        // 获取当前时间
        let currentTime = Date.now();
        let timeUntilExpiry = localStorage.getItem("tokenExpiryTime") - currentTime;
        let refreshInterval = Math.max(timeUntilExpiry - 30000, 0); // 提前30秒刷新Token
      
        // 使用箭头函数来访问组件的this
        localStorage.setItem("refreshTokenTimeout", setTimeout(async () => {
          await fetchToken();
          scheduleTokenRefresh(); // 重新调度下一次刷新
        }, refreshInterval));
      }

      /* 定时获取 Token */
      scheduleTokenRefresh(); 
      // 定时发送异步请求，获取硬件侧的数据
      this.fetchHardSideData();
      this.intervalId = setInterval(this.fetchHardSideData, 600); // 每0.6秒发送一次请求
      
      // 定时发送异步请求，获取AI侧的数据
      // this.fetchDriverStatesData();
      // this.intervalId = setInterval(this.fetchDriverStatesData, 200); // 每0.2秒发送一次请求
    },
    beforeUnmount() {
      // 组件销毁前清除定时器
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
    }
  }
}
</script>

<style>
.whole-container{
  height: 100vh;
  background: linear-gradient(to top right, #0E171F, #132029, #25404C);/*#0E171F*/
  /*title-box & content-box 垂直分布 */
  display: flex;
  flex-direction: column;
  position: relative;
}

/*标题容器*/
.title-box{
  flex-grow: 0.09;
  /*图片和文字水平分布 各占三分之一 */
  display: flex;
  flex-direction: row;
}

/*标题和图片样式:图片和文字水平分布 各占三分之一 */
.flex-item {  
  flex: 1 0 0; /* flex-grow: 1; flex-shrink: 0; flex-basis: 0; */  
  text-align: center; /* 水平居中内容 */  
} 

/*图片样式*/
.img-box1{
  max-width: 70%; /* 防止图片过大 */  
  height: auto; /* 保持图片比例 */
  position: relative;
  top: 10px; 
}
/*标题背景样式*/
.title-bgimg{
  width: 500px;
  height: 50px;
  z-index: -1;
}
/*标题样式*/
.title{
  flex-grow: 1;
  display: inline-block;
  font-size: 20px;
  letter-spacing: 13px;
  font-weight: 700;
  background: linear-gradient(to bottom, #F6B74A, #e75900);  /*渐变颜色*/
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  position: absolute;
  left: 720px;
}

/*内容容器*/
.content-box{
  flex-grow: 1;
  display: flex;
  flex-direction: row;
}

/*健康数据样式*/
.info-box{
  flex-grow: 0.6;
  display: flex;
  flex-direction: column;
}
/*健康数据等分垂直布局*/

/*数据边框动态效果*/
.info-item {
  flex-grow: 1;
  margin-bottom: 10px;
  margin-right: 30px;
  margin-left: 30px;
 /* border: 2px double #595B5D;  1像素宽，实线，黑色 */ 
  position: relative;
  /* 超出隐藏需要加上*/
  overflow: hidden; 
  margin-bottom: -10px;
}
.content {
  text-align: center;
  background: linear-gradient(to bottom,#F1D7B4, #F5BC5C);  /*渐变颜色*/
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  font-size: 20px;
  letter-spacing: 10px;
}
.line {
  /* 结合外层元素的相对定位 */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 1px;
  /* 加上渐变效果，方可形成拖尾效果 */
  background: linear-gradient(90deg, transparent, #ffffff);
}

/*分割线动画效果*/

.divline::before,
.divline::after{
  content: "";  
  position: absolute;  
  width: 100px; /* 初始大小 */  
  height: 2px;  
  background: inherit;  
  background-color:#F6B74A;
  animation: flow 3s linear infinite; /* 应用动画 */
}

.divline::before {  
  left: -100px; /* 初始位置 */  
  animation-direction: reverse; /* 反向动画 */  
}  
  
.divline::after {  
  right: -100px; /* 初始位置 */  
}  

@keyframes flow {  
  0% {  
    width: 100px; /* 动画开始时的大小 */  
  }  
  50% {  
    width: 100%; /* 动画中间时的大小 */  
  }  
  100% {  
    width: 100px; /* 动画结束时的大小 */  
  }  
}

/*实时监控样式*/
.monitor-box{
  flex-grow: 1;
  display: flex;
  flex-direction: column;

}
.video-container{
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.monitor-title{
  flex-grow: 0.05;
  display: flex;
  flex-direction: row;
}
.monitor-img{
  flex-grow: 0.002;
  width: 50px;
  height: 40px;
  position: relative;
  left:180px;
  top:10px;
}
.title-content{
  flex-grow: 1;
  font-size: 20px;
  letter-spacing: 13px;
  font-weight: 700;
  background: linear-gradient(to bottom, #F6B74A, #e75900);  /*渐变颜色*/
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  text-align: center;
}
/*实时监测视频样式 */
.monitor-video{
  flex-grow: 1;
  border: 2px double #595B5D; /* 1像素宽，实线，黑色 */ 
  object-fit: cover; /*后端视频自适应大小*/
  height: 50px;
  width: 100%
}
.indicator-container{
  flex-grow: 0.2;  
  display: flex;  
  flex-direction: row;  
  justify-content: space-between; /* 添加以平均分配按钮之间的空间 */
}
.indicator{
  flex-grow: 1;  
  margin-right: 20px;  
  margin-left: 20px;  
  /* 设置默认背景颜色，或者如果需要的话，移除这一行 */  
  background-color: transparent;  
  border: none; /* 移除默认的边框 */  
  padding: 10px; /* 添加一些内边距以显示背景图像 */
}
.indicator.seatbelt-indicator{
  background-image: url('../assets/other/安全带.svg');
  background-size: contain;
  background-position: center; /* 根据需要调整图片位置 */  
  background-repeat: no-repeat; /* 防止图片重复 */ 
} 
.indicator.tired-indicator{
  position: relative;
  background-image: url('../assets/other/疲劳提醒.svg');
  background-size: contain;
  background-position: center; /* 根据需要调整图片位置 */  
  background-repeat: no-repeat; /* 防止图片重复 */
}
.indicator.smoke-indicator{
  background-image: url('../assets/other/抽烟.svg');
  background-size: contain;
  background-position: center; /* 根据需要调整图片位置 */  
  background-repeat: no-repeat; /* 防止图片重复 */
}
.indicator.drink-indicator{
  background-image: url('../assets/other/喝水.svg');
  background-size: contain;
  background-position: center; /* 根据需要调整图片位置 */  
  background-repeat: no-repeat; /* 防止图片重复 */
}
.indicator.phone-indicator{
  background-image: url('../assets/other/玩手机.svg');
  background-size: contain;
  background-position: center; /* 根据需要调整图片位置 */  
  background-repeat: no-repeat; /* 防止图片重复 */
}
/*/实时监控样式*/


/* 按钮闪烁 */
@keyframes blink {  
  0% {  
    background-color: var(--indicator-off-color);  
  }  
  50% {  
    background-color: var(--indicator-on-color);  
  }  
  100% {  
    background-color: var(--indicator-off-color);  
  }  
}  
.blinking {  
  animation: blink 1s infinite; /* 应用动画 */
   animation-fill-mode: both;  
} 

#app1{
  margin-bottom: -140px;
  position: relative;
  left: 80px;
  top:-20px;
}

#app2{
  margin-bottom: -140px;
  position: relative;
  left: 80px;
  top:-20px;
}

#app3{
  margin-bottom: -140px;
  position: relative;
  left: 80px;
  top:20px
}

#app4{
  margin-bottom: -150px;
  position: relative;
  left: 80px;
  top:-20px
}

#app5{
  margin-bottom: -140px;
  position: relative;
  left: 90px;
  top: -20px;
}

#app6{
  margin-bottom: -150px;
  position: relative;
  left: 80px;
  top: -20px;
}
/*
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}*/
</style>
