<!--本文件为实现温度可视化的图表组件-->
<!--目前本文件展示的是固定温度-->
<!--需要从云端实时获取的数据为temperature 位于本文件的第21行-->
<template>
    <div id="main2" style="width: 210px; height: 210px"></div>
  </template>
  
<script>
    import * as echarts from 'echarts/core';
    import { GaugeChart } from 'echarts/charts';
    import { CanvasRenderer } from 'echarts/renderers';

  
  export default {
    mounted() {
        echarts.use([GaugeChart, CanvasRenderer]);

        var chartDom = document.getElementById('main2');
        var myChart = echarts.init(chartDom);
        var option;
        var temperature = localStorage.getItem('temperature');  //此处的temperature为最终显示到pc界面的值
        var unit = '℃';
        var svgPath = 'path://M570,729.5V86.4c0-42.2-31.4-76.4-70-76.4s-70,34.2-70,76.4v643c-41.7,24.3-70,68.9-70,120.6c0,77.3,62.7,140,140,140s140-62.7,140-140C640,798.3,611.7,753.7,570,729.5z'; //温度计SVG路径
        
        option = {
            title: { //标题样式
                text: `${temperature}${unit}`, //标题
                textStyle: { //标题的样式
                    color: '#F4BF66',
                    fontFamily: 'Microsoft YaHei',
                    align: '#F4BF66',
                    verticalAlign: 'middle'
                },
                subtextStyle: { //副标题的样式
                    color: '#F4BF66',
                    fontSize: 20
                },
                top: '35%',
                left: '55%',
                itemGap: 10, //主副标题之间的间距。
            },
            tooltip: { //提示框浮层属性
                show: true, //默认为true
                transitionDuration: 0.8, //提示框浮层的移动动画过渡时间，单位是 s，设置为 0 的时候会紧跟着鼠标移动
                /*formatter: function(item) { //提示框浮层内容格式器，支持字符串模板和回调函数两种形式
                    return `${temperature}${unit}`;
                }*/
            },
            series: [{
                name: '温度', //系列名称
                type: 'liquidFill', //系列类型
                shape: svgPath, //水填充图的形状 circle默认圆形  rect圆角矩形  triangle三角形  diamond菱形  pin水滴状 arrow箭头状  还可以是svg的path
                center: ['50%', '50%'], //图表相对于盒子的位置[水平, 垂直]，默认是[50%,50%]在水平、垂直方向居中 可设置百分比活着具体数值
                radius: '50%', //图表的大小 值是圆的直径 可以是百分比 也可以是具体值 100%则占满整个盒子 默认是40% 百分比下是根据宽高最小的一个为参照依据
                amplitude: 3, //振幅 是波浪的震荡幅度 可以取具体的值 也可以是百分比 百分比下是按图标的直径来算
                waveLength: '50%', //波的长度 可以是百分比也可以是具体的像素值  百分比下是相对于直径的 取得越大波浪的起伏越小
                phase: 0, //波的相位弧度 默认情况下是自动
                direction: 'left', //波移动的速度 两个参数  left 从右往左 right 从左往右
                waveAnimation: true, //控制波动画的开关，布尔值： false关闭动画，true开启动画（默认值）
                animationEasing: 'linear', //初始动画
                animationEasingUpdate: 'quarticInOut', //数据更新的动画效果
                animationDuration: 2000, //初始动画的时长，支持回调函数，可以通过每个数据返回不同的 delay 时间实现更绚丽的初始动画效果
                animationDurationUpdate: 200, //数据更新动画的时长
                data: [{
                    name: '温度', //数据项名称
                    value: (temperature - 0) / 65, // 原先除以100，改变比例
                    rawValue: temperature     //需要更新的值
                }],
                label: { //图表内部字体
                    normal: {
                        formatter: ''
                    }
                },
                outline: { //轮廓样式
                    show: false, //是否显示轮廓 布尔值
                    borderDistance: 0, //外部轮廓与图表的距离 数字
                    itemStyle: {
                        // borderColor: 'rgba(255,255,255,0.8)', //边框的颜色
                        borderColor: '#fd4d49', //边框的颜色
                        borderWidth: 0, //边框的宽度
                        shadowBlur: 10, //外部轮廓的阴影范围 一旦设置了内外都有阴影
                        shadowColor: new echarts.graphic.LinearGradient(
                            //4个参数用于配置渐变色的起止位置, 依次对应右/下/左/上四个方位
                            0, 0, 0, 1,
                            //数组, 用于配置颜色的渐变过程. 每一项为一个对象, 包含offset和color两个参数. offset的范围是0 ~ 1, 用于表示起始位置
                            [ //外部轮廓的阴影颜色 
                                {
                                    offset: 0,
                                    color: "#cffc03"
                                },
                                {
                                    offset: 1,
                                    color: '#ecfc03'
                                }
                            ]
                        )
                    }
                },
                backgroundStyle: {
                    color: 'transparent', //图表的背景颜色
                    borderWidth: 2, //图表的边框宽度
                    borderColor: 'rgba(255,255,255,0.8)', //图表的边框颜色
                    shadowBlur: 2, //阴影模糊
                    shadowColor: new echarts.graphic.LinearGradient(
                        //4个参数用于配置渐变色的起止位置, 依次对应右/下/左/上四个方位
                        0, 0, 0, 1,
                        //数组, 用于配置颜色的渐变过程. 每一项为一个对象, 包含offset和color两个参数. offset的范围是0 ~ 1, 用于表示起始位置
                        [ //外部轮廓的阴影颜色 
                            {
                                offset: 0,
                                color: "#cffc03"
                            },
                            {
                                offset: 1,
                                color: '#ecfc03'
                            }
                        ]
                    ),
                    itemStyle: {
                        shadowBlur: 10, //设置无效
                        shadowColor: '#f60', //设置无效
                        opacity: 1 //设置无效
                    }
                },
                color: [ //水波的颜色
                    new echarts.graphic.LinearGradient(
                        0, 0, 0, 1,
                        [{
                                offset: 0,
                                color: "#BE7A3D"
                            },
                            {
                                offset: 1,
                                color: '#826634'
                            }
                        ]
                    )
                ],
                itemStyle: {
                    opacity: 0.5, //波浪的透明度
                    shadowBlur: 10, //波浪的阴影范围
                    shadowColor: '#ecfc03' //阴影颜色
                },
                emphasis: {
                    itemStyle: {
                        opacity: 1 //鼠标经过波浪颜色的透明度
                    }
                }
            }]
        }
        option && myChart.setOption(option);

    }
}
  </script>
  
  <style>
  </style>