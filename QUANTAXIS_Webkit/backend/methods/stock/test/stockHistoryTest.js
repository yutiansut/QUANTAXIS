const stock = require('../index').stock;

const query = { code: '600848' };

stock.getHistory(query).then(({ data }) => {
  console.log(data);
});

/** 

const query2 = {
  code: '600848',
  ktype: 'week',
};
stock.getHistory(query2).then(({ data }) => {
  console.log(data);
});

const query3 = {
  code: '600848',
  ktype: '15',
};
stock.getHistory(query3).then(({ data }) => {
  console.log(data);
});


const query3 = {
  code: '600848'
};


function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = year + seperator1 + month + seperator1 + strDate;
    return currentdate;
}





stock.getHistory(query3).then(({ data }) => {
  var datas=data.record;
  var start="2016-12-08";
  var end=getNowFormatDate()
  console.log(end)
  var datas=data.record;
  function getid(date){
  for(i=0;i<datas.length;i++){
      if (datas[i][0]==date){
        console.log(date)
        console.log(i)
        return i
      } 
    }
    }
    var sId=getid(start);
    console.log(sId)
    var eId=getid(end);
    console.log(eId)
    if (i==-100){
      console.log("Wrong Date or No data")
    }
    else{
      var newarray=datas.slice(sId,eId+1)
      console.log(newarray)
    }
});
*/