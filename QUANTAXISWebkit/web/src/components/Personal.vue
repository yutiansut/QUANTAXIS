<template>
    <div id="personal">
        <div class="welcome">
            <mu-list>
                <router-link to="/personal/index">
                    <mu-list-item title="个人中心"></mu-list-item>
                </router-link>
                <router-link to="/personal/notebook">
                    <mu-list-item title="NOTEBOOK"></mu-list-item>
                </router-link>
                <router-link to="/personal/backtest">
                    <mu-list-item title="模拟回测"></mu-list-item>
                </router-link>
    
                <router-link to="/personal/monitor">
                    <mu-list-item title="日线数据"></mu-list-item>
                </router-link>
    
            </mu-list>
            <mu-divider/>
            <mu-list>
                <router-link to="/personal/trade">
                    <mu-list-item title="实盘监控"></mu-list-item>
                </router-link>
                <router-link to="/personal/analysis">
                    <mu-list-item title="复盘分析"></mu-list-item>
                </router-link>
                <router-link to="/personal/stocklist">
                    <mu-list-item title="股票池"></mu-list-item>
                </router-link>
    
                <router-link to="/personal/capital">
                    <mu-list-item title="资金曲线"></mu-list-item>
                </router-link>
                <router-link to="/personal/setting">
                    <mu-list-item title="账户设置"></mu-list-item>
                </router-link>
                <router-link to="/personal/api">
                    <mu-list-item title="APIS"></mu-list-item>
                </router-link>
                <mu-divider/>
            </mu-list>
        </div>
        <div id="view">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
</script>
<style lang="css">
#personal {
    position: relative;
    width: 100%;
    height: 100%;
    display: block;
}

.welcome {
    margin-top: 2%;
    margin-right: 3%;
    width: 18%;
    height: 100%;
    float: left;
    display: inline-block;
}

#view {
    margin-top: 2%;
    width: 60%;
    height: 100%;
    float: left;
    display: inline-block;
}
</style>