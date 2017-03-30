var mongoose = require('mongoose');
var connWsc = mongoose.connect('mongodb://localhost/wsc');
var wscSchema = require('./wscSchema');

var wscQuery = mongoose.model('wasQuery',wscSchema)

module.exports = wscQuery;