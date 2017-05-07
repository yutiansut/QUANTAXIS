<template>
  <div>
    <h1>QUERY</h1>
    <div>
      <ul>
        <li><input v-model="message" v-on:keyup.enter="querybyname($event.currentTarget.value)" placeholder="edit me" lazy></li>
        <li>
          <p>Message is: {{ message }}</p>
        </li>
        <mu-table :height="height" :enableSelectAll="enableSelectAll">
          <mu-thead>
            <mu-tr>
              <mu-th>title</mu-th>
            </mu-tr>
          </mu-thead>
          <template v-for="item in items">

            <mu-tbody>
              <mu-tr>
                <mu-td>{{ item}}</mu-td>
              </mu-tr>
            </mu-tbody>
          </template>

        </mu-table>
        <mu-pagination :total="total" :showSizeChanger="showSizeChanger" :pageSizeOption="pageSizeOption" @pageSizeChange="handleClick">
        </mu-pagination>
      </ul>
    </div>

  </div>
  </div>
</template>
<script>
  import axios from 'axios'

  export default {
    name: 'axios',
    data: function () {
      return {
        height: '300px',
        multiSelectable: true,
        enableSelectAll: false,
        message: 1,
        items: ['1', '2'],
        total: 130,
        current: 1,
        showSizeChanger: true,
        pageSizeOption: [10, 20, 30, 40]
      }
    },
    methods: {
      handleClick(newIndex) {
        console.log('page size change event', newIndex)
      },
      query() {
        axios.get('http://localhost:3000/apis/querytitlebyName?name=%E6%9C%9D%E9%B2%9C')
          .then(function (response) {
            console.log(response.data[1]);
            var data1 = response.data;

            return data1
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      querybyname(message) {
        let val = 'name=' + message
        console.log(val)
        axios.get('http://localhost:3000/apis/querytitlebyName?' + val)
          .then(response => {
            this.items = response.data;
            this.total = this.items.length;
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }
  }
</script>