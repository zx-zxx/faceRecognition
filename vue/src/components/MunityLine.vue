<!--本文件为实现湿度可视化的图表组件-->
<!--目前本文件展示的是固定湿度18.4，单位是参照网上给的标准（因为不清除硬件传过来的具体数据是什么样），如要更改，请定位到第22行-->
<!--需要从云端实时获取的数据为text 位于本文件的第20行-->

<template>  
  <div id="main3" style="width: 210px; height: 210px"></div>  
</template>  
  
<script>  
import * as echarts from 'echarts';  
import 'echarts-liquidfill';  
  
export default {  
  mounted() {  
    const dom = document.getElementById('main3'); // 修改这里以匹配模板中的 id  
    const myChart = echarts.init(dom);  
    const option = {  
      title: [   
        {  
          text: localStorage.getItem('luminance'),   //此处的text为最终显示到pc界面的值
          left: 'center',  
          subtext: 'RH%',   //单位 
          textStyle: {  
            color: '#F4BF66',  
            fontSize: 50,  
          },  
          subtextStyle: {  
            color: '#00b36a',  
            fontSize: 25,  
          },  
        },  
      ],  
      series: [ // 添加 series 配置项  
        {   
          data: [0.184], // 这里的数据应该匹配你的湿度值  
          outline: {  
            borderDistance: 0,  
            itemStyle: {  
              borderWidth: 2,  
              borderColor: '#112165',  
            },  
          },  
          backgroundStyle: {  
            color: 'rgba(220, 220, 220, 0.8)',  
          },  
          label: {  
            show: true,  
            color: '#00b36a',  
            fontSize: 50,  
            formatter: function (params) {  
              return params.value.toFixed(2) + 'RH%'; // 格式化显示的值  
            },  
          },  
        },  
      ],  
    };  
  
    if (option && typeof option === 'object') {  
      myChart.setOption(option);  
    }  
  },  
};  
</script>  
  
<style scoped>  
/* 在这里可以添加你的样式 */  
</style>