<!--本文件为实现心率可视化的图表组件-->
<!--目前本文件展示的是固定心率100，单位和y轴范围的设置是参照网上给的标准（因为不清除硬件传过来的具体数据是什么样），如要更改，请定位到56行、58行、59行-->
<!--需要从云端实时获取的数据为value 位于本文件的第105行-->
<template>
     <div id="main5" style="width: 210px; height: 210px"></div>
  </template>
  
  <script>
    import * as echarts from 'echarts/core';
    import { GridComponent } from 'echarts/components';
    import { LineChart } from 'echarts/charts';
    import { UniversalTransition } from 'echarts/features';
    import { CanvasRenderer } from 'echarts/renderers';

  
  export default {
    mounted() {
       echarts.use([GridComponent, LineChart, CanvasRenderer, UniversalTransition]);

        var chartDom = document.getElementById('main5');
        var myChart = echarts.init(chartDom);
        var data = [30,30,30,30,30,30]; 
        var option;

        // 获取当前时间的字符串表示
        function getCurrentTime() {
            var now = new Date();
            var hours = now.getHours().toString().padStart(2, '0');
            var minutes = now.getMinutes().toString().padStart(2, '0');
            var seconds = now.getSeconds().toString().padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
        }

        var now = new Date(); // 获取当前时间  
        var xAxisData = [];  
        for(let i = 6; i >= 0; i--) {  
            var timestamp = now.getTime() - i * 1000; // 基于当前时间计算过去的时间点  
            var timeString = new Date(timestamp).toLocaleTimeString('en-US', { hour12: false });  
            xAxisData.push(timeString);  
        }

        option = {
            color:'',
            xAxis: {
                type: 'category',
                data: xAxisData,
                axisLabel: {   
                    interval: 0, // 设置为0表示强制显示所有标签  
                    rotate: 45 // 标签之间空间不足，旋转标签  
                },  
                axisTick: {    
                    show: true, // 确保刻度线可见   
                }  
            },
            yAxis: {
                name: '次/分钟',    //心率的单位
                type: 'value',
                min: 20,          //y轴最小刻度
                max: 300,         //y轴最大刻度
                interval: 40,     //相邻刻度之间的距离
                // 隐藏坐标轴分割线  
                splitLine: {  
                    show: false  
                },  
                axisLabel: {  
                    fontSize: 8 ,// 设置字体大小为14像素，您可以根据需要调整这个值  
                    color:'#fff'  
                },
                axisTick: {  
                    show: false, // 确保刻度线可见  
                    lineStyle: {  
                        type: 'dashed', // 设置刻度线为虚线  
                        color: '#fff', // 设置刻度线颜色为白色，确保在深色背景下可见  
                        width: 2 // 设置刻度线宽度，根据需要调整  
                    }  
                }    
            },
            series: [
                {
                data: [50, 70, 34, 48, 35, 47, 60],
                type: 'line',
                lineStyle:{
                    color:'#D4603F',
                },
                itemStyle: { // 设置数据点样式  
                    normal: { // 正常状态下的数据点样式  
                        color: '#C65A3B', // 数据点颜色及透明度  
                        borderColor: '#C65A3B', // 数据点边框颜色  
                        borderWidth: 1 // 数据点边框宽度  
                    },  
                    emphasis: { // 高亮状态下的数据点样式（如鼠标悬停时）  
                        color: '#C65A3B' // 高亮时的数据点颜色及透明度，这里设置为完全不透明  
                    }  
                },  
                label: {  
                    color:'#F4BF66',
                    show: true, // 显示数据点标签  
                    position: 'top' // 标签位置，可以是 'top', 'bottom', 'left', 'right', 'inside', 'insideLeft', 'insideRight', 'insideTop', 'insideBottom', 'insideTopLeft', 'insideTopRight', 'insideBottomLeft', 'insideBottomRight'  
                },  
            }]
        };

        function updateChart(){
            //模拟获取新数据
            var newDataPoint = localStorage.getItem('heartRate');    //此处的newDataPoint为最终显示到pc界面的值
            //更新数据
            data.shift();
            data.push(newDataPoint);
            //更新x轴数据
            xAxisData.shift();
            xAxisData.push(getCurrentTime());
            //更新图标配置项
            option.xAxis.data = xAxisData;
            option.series[0].data = data;
            //刷新图表
            myChart.setOption(option);
            //每秒更新一次数据
            setTimeout(updateChart,1000);
        }

        option && myChart.setOption(option);
        updateChart();

    }    
}
  </script>
  
  <style>
  </style>