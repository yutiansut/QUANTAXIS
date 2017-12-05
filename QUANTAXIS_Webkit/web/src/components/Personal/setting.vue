<template>
  <div>
      <mu-list>
        <mu-list-item disabled title="个人设置" describeText="总是中断"/>
      </mu-list>
      <mu-divider />
      <mu-list>
        <mu-sub-header>声音开启设置</mu-sub-header>
        <mu-list-item disableRipple @click="handleToggle('events')" title="事件和提醒">
          <mu-switch v-model="events"  slot="right"/>
        </mu-list-item>
        <mu-list-item disableRipple @click="handleToggle('calls')" title="电话">
          <mu-switch v-model="calls" slot="right"/>
        </mu-list-item>
        <mu-list-item disableRipple @click="handleToggle('messages')" title="信息">
          <mu-switch v-model="messages" slot="right"/>
        </mu-list-item>
      </mu-list>
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
