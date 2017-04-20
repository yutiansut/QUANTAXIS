<template>
    <div>
        <li v-on:click="query()">{{this.message}}</li>
        <mu-table :height="height">
            <mu-thead>
                <mu-tr>
                    <mu-th>backtest history</mu-th>
                </mu-tr>
            </mu-thead>
            <template v-for="item in items">
                <mu-tbody>
                    <mu-tr>
                        <mu-td>{{item['assest_history']}}</mu-td>
                        <mu-td>{{item['history']}}</mu-td>
                    </mu-tr>
                </mu-tbody>
            </template>
        </mu-table>
    
    </div>
</template>
<script>

import axios from 'axios'

export default {
    data: function () {
        return {
            height: '450px',
            multiSelectable: true,
            enableSelectAll: false,
            message: this.$route.params.id,
            items: [''],
            total: 180,
            current: 1,
            showSizeChanger: true
        }
    },
    methods: {
        query() {
            console.log(this.message)
            let val =this.message
            console.log(val)
            axios.get('http://localhost:3000/backtest/history?cookie='+val)
                    .then(response => {
                        this.items = response.data;
                        console.log(this.items['assest_history'])
                        this.length = this.items.length;
                        
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
        }
    }

}


</script>
