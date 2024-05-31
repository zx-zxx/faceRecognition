<!--本文件为实现血氧可视化的图表组件-->
<!--目前本文件展示的是血氧饱和度，包括单位和参考范围（因为不清除硬件传过来的具体数据是什么样），如要更改，请定位到第18行、19行、106行-->
<!--需要从云端实时获取的数据为value 位于本文件的第112行-->
<template>
    <div id="main6" style="width: 210px; height: 210px"></div>
  </template>
  
<script>
  import * as echarts from 'echarts/core';
  export default {
    mounted() {
      var chartDom = document.getElementById('main6');
      var myChart = echarts.init(chartDom);
      var option;

      option = {
        title: {
          text: "参考范围：",
          subtext:"95%-100%",   //此处是血氧饱和度，如果以ml为单位，请额外修改参考范围
          itemGap: 15,
          left: "center",
          top: 100,
          textStyle: {
            color: 'rgba(246, 183, 74, 0.5)',
            fontSize: 20,
            fontFamily: "宋体",
          },
          subtextStyle: {
            color: "#00000",
            fontSize: 15,
            fontFamily: "Times New Roman",
          },
        },
        series: [
          {
            type: "gauge",
            startAngle: 0.0001,
            endAngle: 0,
            min: 0,
            max: 1,
            splitNumber: 8,
            axisLine: {
              lineStyle: {
                width: 30,
                color: [
                  [0.33, "#FF383C"],
                  [0.66, "#25BD49"],
                  [1, "#FF383C"],
                ],
              },
            },
            pointer: {
              show: false,
              icon: "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
              length: "25%",
              width: 40,
              offsetCenter: [0, "-60%"],
              itemStyle: {
                color: "#000000",
              },
            },
            axisTick: {
              show: false,
              length: 12,
              lineStyle: {
                color: "auto",
                width: 10,
              },
            },
            splitLine: {
              show: false,
              length: 20,
              lineStyle: {
                color: "auto",
                width: 10,
              },
            },
  
            axisLabel: {
              show: false, //设置为false不输出该信息
              color: "#fff",
              fontSize: 20,
              distance: -60,
              formatter: function (value) {
                if (value < 95) {
                  return "血氧饱和度低";
                } else if (value > 100) {
                  return "";
                }
              },
            },
            title: {
              offsetCenter: [-40, "-50%"],  //用于调整白色字体的位置
              fontSize: 15,
              color: "#fff",
            },
            detail: {
              fontSize: 60,
              offsetCenter: [-10, "-30%"],
              valueAnimation: true,
              color: "#C65A3B",
            },
            data: [
              {
                name:
                  "您的血氧饱和度为:" +
                  "\n" +
                  "\n" +
                  "\n" +
                  "\n" +
                  "                                                 %",  //血氧饱和度单位是% 如果是以ml为单位则要看是静脉还是动脉，根据需要修改此处的单位
                value: localStorage.getItem('bloodOxygen'),   //这个value的值为最终显示到pc界面的值
              },
            ],
          },
        ],
        animationDuration: 1000,
      };
      option && myChart.setOption(option);
    }
}
  </script>
  
  <style>
  </style>