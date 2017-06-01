<template>
  <div id="app">
      <mu-appbar title="Title">
      <mu-flat-button color="white" label="QUANTAXIS" style="-webkit-app-region: drag" disable slot="left" />
      <mu-raised-button label="MENU" slot="right" @click="toggle()" />
      <mu-drawer right :open="open" @close="toggle()">
        <mu-appbar title="MENU" />
        <mu-list>
          <router-link to='/personal/index'>
            <mu-list-item title="USER" />
          </router-link>
          <router-link to='/'>
            <mu-list-item title="HOME" />
          </router-link>

          <router-link to='/start'>
            <mu-list-item title="START" />
          </router-link>

          <mu-list-item @click.native="open = false" title="Close" />
        </mu-list>
      </mu-drawer>
    </mu-appbar>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
    name: 'app',
    data() {
      return {
        open: false
      }
    },
    methods: {
      toggle() {
        this.open = !this.open
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

</style>
