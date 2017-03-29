var mongoose = require('mongoose')

var wscSchema = new mongoose.Schema({
	title:{type : Array},
    url:{type : Array},
    content:{type : Array},
    poster:{type : Array},
    viewNum:{type : Array},
    tag:{type : Array},
    time:{type : Array}
})


module.exports = wscSchema;