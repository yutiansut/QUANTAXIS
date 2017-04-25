<template>
    <div id="index">
        <div id="logo">
            <mu-list>
            <mu-list-item  disabled >
                Hi! {{items.user}}
            </mu-list-item>
            </mu-list>
        </div>
        <div id="personal-content">
            <ul>
                <li>策略收益</li>
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
                                <mu-td>S6001ZH60001</mu-td>
                                <mu-td>上证股票组合</mu-td>
                                <mu-td>Employed</mu-td>
                                </mu-tr>
                                <mu-tr>
                                <mu-td>S6001ZH60002</mu-td>
                                <mu-td>上证股票组合</mu-td>
                                <mu-td>Stopped</mu-td>
                                </mu-tr>
                                </mu-tbody>
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
import myron from '../assets/QUANTAXIS.jpg'
import axios from 'axios'
export default {
  data () {
    return {
        items:{
            user:sessionStorage.user
        },
      myron
    }
  }
}
</script>
<style lang="css">
    #logo{
        width:20%;
        height: 20%;
    }
    .mu-item{
        font-size:30px;
    }
    #personal-content{
        margin-top: 2%;
    }
</style>