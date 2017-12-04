<template>
  <div style="text-align:left">
      <h1>{{this.title}}</h1>
      <div class="container">

      <router-link :to="{name:'history',params: {id:this.data0}}">
        <mu-raised-button label="成交明细" class="demo-raised-button" primary/>
      </router-link>
      <router-link :to="{ name:'visual',params: {id:this.data0}}">
          <mu-raised-button label="账户表现" class="demo-raised-button" secondary/>
      </router-link>
      <router-link :to="{name:'strategy',params: {id:this.data0}}">
        <mu-raised-button label="策略查看" class="demo-raised-button" />
      </router-link>

      <mu-divider />
    </div>
      <div>

        <h4>Version: {{this.version}}    Topic:{{this.topic}}
            Last_modified_time:{{this.last_modified_time}}</h4>
      </div>


      <MonacoEditor
      height="600"
      text-align='left'
      theme='vs'
      language="python"
      :code="code"
      :editorOptions="options"
      @mounted="onMounted"
      @codeChange="onCodeChange"
      >{{this.code}}
  </MonacoEditor>
  </div>
</template>





<script>
  import MonacoEditor from 'vue-monaco-editor'
  import axios from 'axios'
  import markdownEditor from 'vue-simplemde/src/markdown-editor'


  // 基础用法
  export default {
    components: {
      MonacoEditor
    },
    data() {
      return {
        code: '//QUANTAXIS CODE EDITOR! \n',
        theme:'vs',
        title:'',
        version:'',
        topic:'',
        data0: this.$route.params.id,
        last_modified_time:'',
        options: {

          selectOnLineNumbers:true,
          roundedSelection: false,
          readOnly: true,
          cursorStyle: 'line',
          automaticLayout: false,
          glyphMargin: true,
          theme:'vs'
        },

      }
    },
    methods: {

      onMounted(editor) {
        this.editor = editor;
      },
      onCodeChange(editor) {
        console.log(editor.getValue());

      },
      ready(id) {
        axios.get('http://localhost:3000/backtest/strategy?cookie=' + id)
          .then(response => {

            this.title = response.data[0]['name']
            this.code = response.data[0]['content']
            this.version= response.data[0]['version']
            this.topic= response.data[0]['topic']
            this.last_modified_time= response.data[0]['datetime']
            console.log(response.data)
          })


      },


    },


    mounted() {
      this.$nextTick(function () {
        this.ready(this.$route.params.id);


      })
    },
    watch: {
      topPopup(val) {
        if (val) {
          setTimeout(() => {
            this.topPopup = false
          }, 800)
        }
      },
      content: function (val, oldVal) {
        setTimeout(() => {
        this.save()
      }, 800)
      }
    }


  }

</script>

<style>

    .monaco-editor vs{
      text-align:left;
    }
    .container {
      display: flex;
      flex-wrap: wrap;
  }
</style>
