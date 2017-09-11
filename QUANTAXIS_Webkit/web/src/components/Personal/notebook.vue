<template>
  <div>
    <h2 align='left'>> NOTEBOOK</h2>

    <mu-paper>
        <mu-text-field v-on:keyup.enter='querycontent($event.currentTarget.value)' hintText="搜索文章" class="demo-divider-form" :underlineShow="false" v-model="message"  />
    </mu-paper>
    <div class="container">

      <mu-flat-button label="NEW" v-on:click='insert_pages()' class="demo-flat-button" />
      <mu-flat-button label="DELETE" class="demo-flat-button" />
    </div>

    <mu-table multiSelectable enableSelectAll ref="table">
      <mu-thead>
        <mu-tr>
          <mu-th>title</mu-th>
          <mu-th>content</mu-th>
        </mu-tr>
      </mu-thead>
      <template v-for="item in items">
      <mu-tbody >
        <mu-tr>
          <router-link :to="{ name:'markdown',params: {id:item['_id']}}">
          <mu-td>{{item['title']}}</mu-td>
          <mu-td>{{item['content']}}</mu-td>
          </router-link>
        </mu-tr>

      </mu-tbody>
      </template>
    </mu-table>

  </div>

</template>

<style>
  .container {
    display: flex;
  }

  .demo-flat-button {
    margin: 12px;
  }

</style>
<script>
  import axios from 'axios'

  export default {
    data: function () {
      return {
        height: '500px',
        multiSelectable: true,
        enableSelectAll: false,
        message: '',
        messages: '',
        items: [''],
        total: 180,
        current: 1,
        showSizeChanger: true
      }
    },
    methods: {
      insert_pages() {
        axios.get('http://localhost:3000/notebook/new?title=' +'new')
          .then(response => {
            var _id = response.data['_id'];
            this.$router.push({name:'markdown',params: {id:_id}})
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      querycontent(mes){
        console.log(mes)
        console.log(this.message)
        axios.get('http://localhost:3000/notebook/querycontent?content='+mes)
          .then(response => {
            this.items = response.data;

          })
          .catch(function (error) {
            console.log(error);
          });
      },
      query() {

        axios.get('http://localhost:3000/notebook/queryall')
          .then(response => {
            this.items = response.data;
            console.log(this.items)
          })
          .catch(function (error) {
            console.log(error);
          });
      }

    },
    mounted(){
      this.$nextTick(function () {
           this.query()

        })
    }
  }

</script>
