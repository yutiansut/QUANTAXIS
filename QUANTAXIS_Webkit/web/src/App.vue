<template>
  <div>
    <mu-appbar title="Title">
      <mu-flat-button class="quantaxislogo" href='https://github.com/yutiansut/quantaxis' target="view_window" color="white" style="-webkit-app-region: drag"
        disable slot="left">QUANTAXIS</mu-flat-button>
      <mu-raised-button slot='right' label="User" ref="button" @click="toggle"/>
      <mu-popover :trigger="trigger" :open="open" @close="handleClose">
          <mu-menu>
            <router-link to='/personal/index'>
              <mu-list-item title="用户中心" />
            </router-link>
            <router-link to='/personal/setting'>
            <mu-menu-item title="Settings" /></router-link>
            <mu-menu-item title="Sign out" @click="signout" />
          </mu-menu>
        </mu-popover>
    </mu-appbar>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'app',
    data() {
      return {
        open: false,
        docked: true,
        item: '登录',
        trigger:null
      }
    },
    mounted () {
      this.trigger = this.$refs.button.$el
    },
    methods: {
      toggle () {
        this.open = !this.open
      },
      handleClose (e) {
        this.open = false
      },
      signout(){
        sessionStorage.clear()
        this.$router.push('/sign');
      }
    },

    watch: {
      topPopup(val) {
        if (val) {
          setTimeout(() => {
            this.item = '注销'
          }, 800)
        }
      }
    }
  }

</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  .mu-flat-button-wrapper {
    font-size: 1.8em;
  }


  .mu-item-content {
    font-size: 18px;
    text-align: middle;
  }

  .user_pad{
    background-color:#2c3e50
  }
  .demo-paper {
    display: inline-block;
    height: 100px;
    width: 100px;
    margin: 20px;
    text-align: center;
  }
  .mu-circle{
    margin: 0 auto;

  }
</style>
