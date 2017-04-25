<template>

<div class="demo-step-container">
    <div id="title">
        <h1>#Start</h1>
        <h2>Only Three Steps,Start your QUANTAXIS</h2>
    </div>
    <div id="content">
    <mu-stepper :activeStep="activeStep" orientation="vertical">
        <mu-step>
            <mu-step-label>
                下载|Download
            </mu-step-label>
            <mu-step-content>
                <p>
                    Github fork & clone
                </p>
                <mu-raised-button label="NEXT" class="demo-step-button" @click="handleNext" primary/>
            </mu-step-content>
        </mu-step>
        <mu-step>
            <mu-step-label>
                安装依赖项|Install Dependences
            </mu-step-label>
            <mu-step-content>
                <p>
                    npm run install | npm run Xweb
                </p>
                <mu-raised-button label="NEXT" class="demo-step-button" @click="handleNext" primary/>
                <mu-flat-button label="BACK" class="demo-step-button" @click="handlePrev" />
            </mu-step-content>
        </mu-step>
        <mu-step>
            <mu-step-label>
                启动可视化网站|Start Journey
            </mu-step-label>
            <mu-step-content>
                <p>
                    npm run all | npm run Xweb
                </p>
                <mu-raised-button label="Finish" class="demo-step-button" @click="handleNext" primary/>
                <mu-flat-button label="BACK" class="demo-step-button" @click="handlePrev" />
            </mu-step-content>
        </mu-step>
    </mu-stepper>
    <p v-if="finished">
        都完成啦!<a href="javascript:;" @click="reset">点这里</a>访问教程
    </p>
    </div>
</div>
</template>

<script>
export default {
  name:'process',
  data () {
    return {
      activeStep: 0
    }
  },
  computed: {
    content () {
      let message = ''
      switch (this.activeStep) {
        case 0:
          message = 'SETTING Environment git clone https://github.com/yutiansut/QUANTAXIS_SPIDER'
          break
        case 1:
          message = 'powershell>install.ps1'
          break
        case 2:
          message = 'powershell>start'
          break
        default:
          message = 'fuck! 又 TM 出错了！！！'
          break
      }
      return message
    },
    finished () {
      return this.activeStep > 2
    }
  },
  methods: {
    handleNext () {
      this.activeStep++
    },
    handlePrev () {
      this.activeStep--
    },
    reset () {
      this.activeStep = 0
    }
  }
}
</script>

<style>
.demo-step-container {
    position:relative;
    width: 100%;
    height: 100%;
    display: block;
}
#title{
    position:relative;
    width:60%;
    height:100%;
    float: left;
    display: inline-block;
    margin: 10% 0%;
}

#content{
    width:30%;
    height:100%;
    position:relative;
    display: inline-block;
    margin: 16% 0%;
}

#title h1{
    color: darkgrey;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 85px;
}

#title h2{
    color: darkgrey;
    font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 20px;

}
#content.demo-step-content {
  margin: 0  16px;
}

#content.demo-step-button {
  margin-top: 12px;
  margin-right: 12px;
}
</style>