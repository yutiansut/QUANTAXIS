<template>
    <div id="index">
        <div id="logo">
            <mu-list>
                <h2 align='left'>> Hi! {{itemd.user}}</h2>
            </mu-list>
        </div>
        <div id="personal-content">
            <ul>
                <mu-table :height="height">
    
                    <template v-for="item in items">
                            <mu-thead>
                                <mu-tr>
                                    <mu-th>strategy</mu-th>
                                    <mu-th>start</mu-th>
                                    <mu-th>end</mu-th>
                                    <mu-th>annualized_returns</mu-th>
                                </mu-tr>
                            </mu-thead>
                        <mu-tbody>

                            <mu-tr>
                                <router-link :to="{ name:'history',params: {id:item['account_cookie']}}">
                                   
                                    <mu-td>{{ item['strategy']}}</mu-td>
                                    <mu-td>{{ item['start_time']}}</mu-td>
                                    <mu-td>{{ item['end_time']}}</mu-td>
                                    <mu-td>{{ item['annualized_returns']}}</mu-td>
    
                                </router-link>
                            </mu-tr>
                        </mu-tbody>
    
                    </template>
    
                </mu-table>
                <li>爬虫状况</li>
                <mu-table>
                    <mu-thead>
                        <mu-tr>
                            <mu-th>ID</mu-th>
                            <mu-th>Name</mu-th>
                            <mu-th>Status</mu-th>
                        </mu-tr>
                    </mu-thead>
                    <mu-tbody>
                        <mu-tr>
                            <mu-td>S6001C0001</mu-td>
                            <mu-td>华尔街中文网爬虫</mu-td>
                            <mu-td>Stopped</mu-td>
                        </mu-tr>
                    </mu-tbody>
                </mu-table>
                <li>回测概览</li>
            </ul>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            itemd: {
                user: sessionStorage.user
            },
            items: ['']

        }
    },
    methods: {
        ready() {

            axios.get('http://localhost:3000/backtest/info?name=' + sessionStorage.user)
                .then(response => {
                    this.items = response.data;
                    console.log(this.items)
                    this.length = this.items.length;
                    var performance = response.data[0]['performance'];
                    console.log(performance)
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },

    mounted() {
        this.$nextTick(function () {
            this.ready();

        })
    }
}

</script>
<style lang="css">
#logo {
    width: 20%;
    height: 20%;
}

.mu-item {
    font-size: 2em;
}

#personal-content {
    margin-top: 2%;
}

li {
    float: left;
}
</style>