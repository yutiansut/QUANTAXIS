<template>
    <div id="index">

        <div id="personal-content">
            <ul>
                <li>策略收益</li>
                    <mu-table>
                        <mu-thead>
                            <mu-tr>
                                <mu-th>ID</mu-th>
                                <mu-th>策略</mu-th>
                                <mu-th>用户</mu-th>
                                <mu-th>开始</mu-th>
                                <mu-th>结束</mu-th>
                                <mu-th>总利润</mu-th>
                                <mu-th>年收益</mu-th>
                                <mu-th>胜率</mu-th>
                                <mu-th>最大回撤</mu-th>
                                <mu-th>Vol</mu-th>
                            </mu-tr>
                        </mu-thead>
                        <mu-tbody>
                            <mu-tr>
                                <mu-td>z</mu-td>
                                <mu-td>BLEX</mu-td>
                                <mu-td>yutiansut</mu-td>
                                <mu-td>2010/01/01</mu-td>
                                <mu-td>2015/01/28</mu-td>
                                <mu-td>40%</mu-td>
                                <mu-td>20%</mu-td>
                                <mu-td>1.13</mu-td>
                                <mu-td>13.6%</mu-td>
                                <mu-td>0.005</mu-td>
                            </mu-tr>

                        </mu-tbody>
                    </mu-table>

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
    
    .mu-item{
        font-size:10px;
    }
    #personal-content{
        margin-top: 2%;
    }
</style>