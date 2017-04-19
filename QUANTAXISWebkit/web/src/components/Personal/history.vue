<template>
<li>11</li>
</template>
<script>

export default{
 ready: function(){
        console.log('deviceid: ' + this.$route.query.cookie);

    }
}
</script>
