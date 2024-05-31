<!--本文件为实现酒精浓度可视化的图表组件-->
<!--目前人为设置浓度为80，单位为%，仪表盘范围为0-100（请根据硬件传输回的实际数据单位修改这部分参数值，包括给仪表盘修改一个合适的范围）
    如要更改，请定位到第30行、31行、32行、
-->
<!--需要从云端实时获取的数据为value 位于本文件的第125行-->
<template>
  <div id="main1" style="width: 210px; height: 210px"></div>
</template>

<script>
import * as echarts from 'echarts/core';
import { GaugeChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

export default {
  /*添加代码，让父组件传数据给子组件*/
  props: ['alcoholVolumn'], // 用来接收父组件给子组件的数据

  mounted() {
    echarts.use([GaugeChart, CanvasRenderer]);

    var chartDom = document.getElementById('main1');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
      // 你现有的选项对象
      series: [
    {
      data: [
        {
          value: localStorage.getItem('alcoholVolumn')    //这个value的值为最终显示到pc界面的值
        }
      ],
      type: 'gauge',  //指定图表类型为仪表盘
      startAngle: 180, //指定仪表盘起始角度（180：正上方）
      endAngle: 0, //指定仪表盘结束角度（0：正下方）
      min: 0, //仪表盘最小值
      max: 100, //仪表盘最大值
      splitNumber: 10, //刻数分割数量
      //元素样式
      itemStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
          offset: 0,
          color: '#C99141' // 起始颜色
        }, {
          offset: 0.5,
          color: '#A94E35' // 中间颜色
        }, {
          offset: 1,
          color: '#C99141' // 结束颜色
          }]
        },
        shadowColor: '#C99141',
        shadowBlur: 10,
        shadowOffsetX: 2,
        shadowOffsetY: 2
      },
      //进度条样式
      progress: {
        show: true, //控制是否显示进度条
        roundCap: true, //控制进度条末端是否为圆形
        width: 10 //进度条宽度
      },
      // 指针
      pointer: {
        icon: 'path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z',//设置指针的图标
        length: '75%',//指针的长度
        width: 10, //指针的宽度
        offsetCenter: [0, '5%'] //指针相对于仪表盘中心的偏移量
      },
      //刻度
      axisLine: {
        roundCap: true,  //控制末端是否为圆形
        lineStyle: {
          width: 10  //刻度的宽度
        }
      },
      //刻度标记
      axisTick: {
        splitNumber: 2, //刻度标记的分割数量
        lineStyle: {
          width: 2,  //刻度标记先宽度
          color: '#999' //刻度标记线颜色
        }
      },
      //分隔线
      splitLine: {
        length: 12,
        lineStyle: {
          width: 3,
          color: '#999'
        }
      },
      axisLabel: {
        distance: 15,
        color: '#999',
        fontSize: 6
      },
      title: {
        show: false
      },
      detail: {
        width: '100%',
        lineHeight: 50,
        height: 30,
        offsetCenter: [0, '35%'],
        valueAnimation: true,
        formatter: function (value) {  
          var unit = 'kg';            // 假设单位是千克 ，可自行修改
          return value + unit;  
        },
        rich: {
          value: {
            fontSize: 25,
            fontWeight: 'bolder',
            color: '#F4BF66'
          },
          unit: {
            fontSize: 20,
            color: '#F4BF66',
            padding: [0, 0, 0, 10]
          }
        }
      }
    }
  ]
};

    function updateChart() {
      //模拟获取新数据
      var newDataPoint =  localStorage.getItem('alcoholVolumn');    //此处的newDataPoint为最终显示到pc界面的值
      // //更新数据
      // data.shift();
      // data.push(newDataPoint);
      //更新图标配置项
      option.series[0].data.value = newDataPoint;
      //刷新图表
      myChart.setOption(option);
      
      setTimeout(updateChart,600);    //每1s更新一次数据
    }

    option && myChart.setOption(option);
    updateChart();
  }
}
</script>

<style>
</style>