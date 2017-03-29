<template>
  <div id="app">
  <mu-appbar title="Title">
    <mu-flat-button color="white" label="QUANTAXIS" style="-webkit-app-region: drag" disable slot="left"/> 
    <mu-raised-button label="MENU"slot="right" @click="toggle()"/>
    <mu-drawer right :open="open" @close="toggle()">
      <mu-appbar title="MENU"/>
      <mu-list>
        <router-link to='/personal/index'><mu-list-item title="USER" /></router-link>
        <router-link to='/'><mu-list-item title="HOME"/></router-link>
        
        <router-link to='/start'><mu-list-item title="START"/></router-link>
        <router-link to='/todo'><mu-list-item title="TODO"/></router-link>
        <mu-list-item @click.native="open = false" title="Close"/>
      </mu-list>
    </mu-drawer>
  </mu-appbar>
    <div class="container">
      <router-view></router-view>
    </div>
            
  </div>
</template>

<script>
  export default {
    data () {
    return {
      open: false
    }
  },
  methods: {
    toggle () {
      this.open = !this.open
    }
  }
  }
</script>

<style>
  @import url(https://fonts.googleapis.com/css?family=Lato:300);
  * {
    margin: 0;
    padding: 0;
  }
  html,
  body { height: 100%; }
  body {
    background:
      radial-gradient(
        ellipse at center,
        rgba(255, 255, 255, 1) 0%,
        rgba(229, 229, 229, .85) 100%
      );
    background-position: center;
    display: flex;
    font-family: Lato, Helvetica, sans-serif;
    justify-content: center;
    text-align: center;
  }
span.mu-flat-button-label{
  font-size: 28px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  width:100%;
}
h1, h2 {
  font-weight: normal;
}
.appbar-search-field{
  color: #FFF;
  margin-bottom: 0;
  &.focus-state {
    color: #FFF;
  }
  .mu-text-field-hint {
    color: fade(#FFF, 54%);
  }
  .mu-text-field-input {
    color: #FFF;
  }
  .mu-text-field-focus-line {
    background-color: #FFF;
  }
}
.mu-raised-button{
  background-color: red;
  color:#FFF;
  }
button.mu-raised-button.hover{
  color:#000000;
}
</style>