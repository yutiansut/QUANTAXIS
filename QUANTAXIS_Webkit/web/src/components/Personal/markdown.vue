<template>
  <markdown-editor  id='markdown' :highlight="true"  v-model="content" ref="markdownEditor":configs="configs"></markdown-editor>
</template>

<script>
  import hljs from 'highlight.js';

  window.hljs = hljs;
  import markdownEditor from 'vue-simplemde/src/markdown-editor'

  // 基础用法
  export default {
    components: {
      markdownEditor
    },
    data () {
      return {
        content: '',
        configs: {
          spellChecker: false // 禁用拼写检查
        }
      }
    }
  }
</script>

<style>
  @import '~simplemde-theme-base/dist/simplemde-theme-base.min.css';
  @import '~github-markdown-css';
  @import '~highlight.js/styles/atom-one-dark.css';
  @import '~simplemde/dist/simplemde.min.css';


.CodeMirror-sizer {
  text-align:left;
  position: relative;
}
.CodeMirror-scroll{
  text-align:left;
  position: relative;
}
.markdown-editor{
  text-align:left;
  text-overflow:scrollable;
  position: relative;
}

  /* 高亮主题可选列表：https://github.com/isagalaev/highlight.js/tree/master/src/styles */
</style>

