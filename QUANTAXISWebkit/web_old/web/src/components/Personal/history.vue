<template>
    <div>
        <div class="container">
            <router-link :to="{ name:'visual',params: {id:this.message}}">
                <mu-raised-button label="账户表现" class="demo-raised-button" secondary/>
            </router-link>
            <mu-raised-button v-on:click='query()' label="成交明细" class="demo-raised-button" />
            <mu-divider />
        </div>
        <mu-table :height="height">
            <mu-thead>
                <mu-tr>
                    <mu-th>backtest history</mu-th>
                </mu-tr>
            </mu-thead>
            <template v-for="item in items">
                <mu-tbody>
                    <mu-tr>
                        <mu-td>{{item[0]}}</mu-td>
                        <mu-td>{{item[1]}}</mu-td>
                        <mu-td>{{item[2]}}</mu-td>
                        <mu-td>{{item[3]}}</mu-td>
                        <mu-td>{{item[4]}}</mu-td>

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
                height: '800px',
                multiSelectable: true,
                enableSelectAll: false,
                message: this.$route.params.id,
                items: [''],
                acc: [''],
                total: 180,
                current: 1,
                showSizeChanger: true
            }
        },
        methods: {
            query() {
                console.log(this.message)
                let val = this.message
                console.log(val)
                axios.get('http://localhost:3000/backtest/history?cookie=' + val)
                    .then(response => {
                        this.items = response.data['history'];
                        this.acc = response.data;
                        //console.log(this.items)
                        //this.length = this.items.length;

                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }

    }
</script>
<style>
    .container {
        display: flex;
        flex-wrap: wrap;
    }
</style>