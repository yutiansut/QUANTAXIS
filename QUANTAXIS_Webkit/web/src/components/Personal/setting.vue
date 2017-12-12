<template>
  <div>
      <mu-list>
        <mu-list-item disabled title="推送设置" describeText="暂时无法使用"/>
      </mu-list>
      <mu-divider />

      <mu-list>
        <mu-sub-header>通知设置</mu-sub-header>

        <mu-list-item disableRipple @click="handleToggle('notifications')"  title="通知">
          <mu-switch v-model="notifications" slot="right"/>
        </mu-list-item>
        <mu-list-item disableRipple @click="handleToggle('trades')"  title="实盘交易推送">
          <mu-switch v-model="trades" slot="right"/>
        </mu-list-item>
        <mu-list-item disableRipple @click="handleToggle('backtestMessages')" title="回测推送">
          <mu-switch v-model="backtestMessages" slot="right"/>
        </mu-list-item>
      </mu-list>
    </div>
  </template>

  <script>

  export default {
    data () {
      return {
        events: Boolean(sessionStorage.getItem('trades')),
        calls:  Boolean(sessionStorage.calls),
        messages: Boolean(sessionStorage.messages),
        notifications: Boolean(sessionStorage.notifications),
        trades: Boolean(sessionStorage.trades),
        backtestMessages: Boolean(sessionStorage.backtestMessages)
      }
    },
    methods: {
      handleToggle (key) {
        //this[key] = !this[key]

        sessionStorage.setItem(key,!Boolean(this[key]))
        console.log(this[key])
      }
    },
    mounted () {

      sessionStorage.setItem('events',false)

      sessionStorage.setItem('calls',false)
      sessionStorage.setItem('messages',false)
      sessionStorage.setItem('notifications',false)
      sessionStorage.setItem('trades',false)
      sessionStorage.setItem('backtestMessages',false)
      console.log(Boolean(sessionStorage.getItem('trades')))
    },
    watch(){

    }

  }
  </script>
