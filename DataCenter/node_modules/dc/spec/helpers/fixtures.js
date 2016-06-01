/* jscs:disable validateQuoteMarks, maximumLineLength */
/* jshint -W109, -W101, -W098 */
function dateCleaner (e) {
    e.dd = d3.time.format.iso.parse(e.date);
}

function loadDateFixture () {
    var fixture = JSON.parse("[" +
        "{\"value\":\"44\",\"nvalue\":\"-4\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"T\",\"id\":1,\"region\":\"South\",\"date\":\"2012-05-25T16:10:09Z\"}, " +
        "{\"value\":\"22\",\"nvalue\":\"-2\",\"countrycode\":\"US\",\"state\":\"Colorado\",\"status\":\"F\",\"id\":2,\"region\":\"West\",\"date\":\"2012-06-10T16:10:19Z\"}, " +
        "{\"value\":\"33\",\"nvalue\":\"1\",\"countrycode\":\"US\",\"state\":\"Delaware\",\"status\":\"T\",\"id\":3,\"region\":\"West\",\"date\":\"2012-08-10T16:20:29Z\"}, " +
        "{\"value\":\"44\",\"nvalue\":\"-3\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"F\",\"id\":4,\"region\":\"South\",\"date\":\"2012-07-01T16:10:39Z\"}, " +
        "{\"value\":\"55\",\"nvalue\":\"-5\",\"countrycode\":\"CA\",\"state\":\"Ontario\",\"status\":\"T\",\"id\":5,\"region\":\"Central\",\"date\":\"2012-06-10T16:10:49Z\"}, " +
        "{\"value\":\"66\",\"nvalue\":\"-4\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"F\",\"id\":6,\"region\":\"West\",\"date\":\"2012-06-08T16:10:59Z\"}, " +
        "{\"value\":\"22\",\"nvalue\":\"10\",\"countrycode\":\"CA\",\"state\":\"Ontario\",\"status\":\"T\",\"id\":7,\"region\":\"East\",\"date\":\"2012-07-10T16:10:09Z\"}, " +
        "{\"value\":\"33\",\"nvalue\":\"1\",\"countrycode\":\"US\",\"state\":\"Mississippi\",\"status\":\"F\",\"id\":8,\"region\":\"Central\",\"date\":\"2012-07-10T16:10:19Z\"}, " +
        "{\"value\":\"44\",\"nvalue\":\"2\",\"countrycode\":\"US\",\"state\":\"Mississippi\",\"status\":\"T\",\"id\":9,\"region\":\"Central\",\"date\":\"2012-08-10T16:30:29Z\"}, " +
        "{\"value\":\"55\",\"nvalue\":\"-3\",\"countrycode\":\"US\",\"state\":\"Oklahoma\",\"status\":\"F\",\"id\":10,\"region\":\"\",\"date\":\"2012-06-10T16:10:39Z\"}" +
        "]");

    fixture.forEach(dateCleaner);
    return fixture;
}

function loadDateFixture2 () {
    var fixture = JSON.parse(
        "[" +
            "{\"value\":\"11\",\"nvalue\":\"-4\",\"countrycode\":\"UK\",\"state\":\"Liverpool\",\"status\":\"T\",\"id\":11,\"region\":\"South\",\"date\":\"2012-05-25T16:20:09Z\"}, " +
            "{\"value\":\"76\",\"nvalue\":\"-1\",\"countrycode\":\"UK\",\"state\":\"London\",\"status\":\"F\",\"id\":12,\"region\":\"\",\"date\":\"2012-06-10T16:20:39Z\"}" +
            "]");

    fixture.forEach(dateCleaner);
    return fixture;
}

function loadBoxPlotFixture () {
    return JSON.parse("[" +
        "{\"value\":\"44\",\"nvalue\":\"-4\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"T\",\"id\":1,\"region\":\"South\",\"date\":\"2012-05-25T16:10:09Z\"}, " +
        "{\"value\":\"22\",\"nvalue\":\"-2\",\"countrycode\":\"US\",\"state\":\"Colorado\",\"status\":\"F\",\"id\":2,\"region\":\"West\",\"date\":\"2012-06-10T16:10:19Z\"}, " +
        "{\"value\":\"33\",\"nvalue\":\"1\",\"countrycode\":\"US\",\"state\":\"Delaware\",\"status\":\"T\",\"id\":3,\"region\":\"West\",\"date\":\"2012-08-10T16:20:29Z\"}, " +
        "{\"value\":\"44\",\"nvalue\":\"-3\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"F\",\"id\":4,\"region\":\"South\",\"date\":\"2012-07-01T16:10:39Z\"}, " +
        "{\"value\":\"55\",\"nvalue\":\"-5\",\"countrycode\":\"US\",\"state\":\"Ontario\",\"status\":\"T\",\"id\":5,\"region\":\"Central\",\"date\":\"2012-06-10T16:10:49Z\"}, " +
        "{\"value\":\"66\",\"nvalue\":\"-4\",\"countrycode\":\"US\",\"state\":\"California\",\"status\":\"F\",\"id\":6,\"region\":\"West\",\"date\":\"2012-06-08T16:10:59Z\"}, " +
        "{\"value\":\"33\",\"nvalue\":\"10\",\"countrycode\":\"US\",\"state\":\"Ontario\",\"status\":\"T\",\"id\":7,\"region\":\"East\",\"date\":\"2012-07-10T16:10:09Z\"}, " +
        "{\"value\":\"33\",\"nvalue\":\"1\",\"countrycode\":\"US\",\"state\":\"Mississippi\",\"status\":\"F\",\"id\":8,\"region\":\"Central\",\"date\":\"2012-07-10T16:10:19Z\"}, " +
        "{\"value\":\"44\",\"nvalue\":\"2\",\"countrycode\":\"US\",\"state\":\"Mississippi\",\"status\":\"T\",\"id\":9,\"region\":\"Central\",\"date\":\"2012-08-10T16:30:29Z\"}, " +
        "{\"value\":\"1\",\"nvalue\":\"-12\",\"countrycode\":\"US\",\"state\":\"Washington\",\"status\":\"F\",\"id\":12,\"region\":\"\",\"date\":\"2012-06-10T16:10:39Z\"}, " +
        "{\"value\":\"144\",\"nvalue\":\"-3\",\"countrycode\":\"US\",\"state\":\"Massachusetts\",\"status\":\"T\",\"id\":15,\"region\":\"\",\"date\":\"2012-06-10T16:10:39Z\"}, " +
        "{\"value\":\"1\",\"nvalue\":\"-4\",\"countrycode\":\"CA\",\"state\":\"California\",\"statCA\":\"T\",\"id\":1,\"region\":\"South\",\"date\":\"2012-05-25T16:10:09Z\"}, " +
        "{\"value\":\"2\",\"nvalue\":\"-2\",\"countrycode\":\"CA\",\"state\":\"Colorado\",\"statCA\":\"F\",\"id\":2,\"region\":\"West\",\"date\":\"2012-06-10T16:10:19Z\"}, " +
        "{\"value\":\"3\",\"nvalue\":\"1\",\"countrycode\":\"CA\",\"state\":\"Delaware\",\"statCA\":\"T\",\"id\":3,\"region\":\"West\",\"date\":\"2012-08-10T16:20:29Z\"}" +
        "]");
}

function loadColorFixture () {
    return JSON.parse("[" +
        "{\"colData\":\"1\", \"rowData\": \"1\", \"colorData\": \"1\"}," +
        "{\"colData\":\"1\", \"rowData\": \"1\", \"colorData\": \"1\"}," +
        "{\"colData\":\"1\", \"rowData\": \"2\", \"colorData\": \"2\"}," +
        "{\"colData\":\"1\", \"rowData\": \"2\", \"colorData\": \"2\"}," +
        "{\"colData\":\"2\", \"rowData\": \"1\", \"colorData\": \"3\"}," +
        "{\"colData\":\"2\", \"rowData\": \"1\", \"colorData\": \"3\"}," +
        "{\"colData\":\"2\", \"rowData\": \"2\", \"colorData\": \"4\"}," +
        "{\"colData\":\"2\", \"rowData\": \"2\", \"colorData\": \"4\"}" +
        "]");
}

function loadColorFixture2 () {
    return JSON.parse("[" +
        "{\"colData\":\"3\", \"rowData\": \"3\", \"colorData\": \"5\"}," +
        "{\"colData\":\"3\", \"rowData\": \"4\", \"colorData\": \"5\"}," +
        "{\"colData\":\"4\", \"rowData\": \"5\", \"colorData\": \"6\"}," +
        "{\"colData\":\"4\", \"rowData\": \"6\", \"colorData\": \"6\"}," +
        "{\"colData\":\"5\", \"rowData\": \"3\", \"colorData\": \"7\"}," +
        "{\"colData\":\"5\", \"rowData\": \"4\", \"colorData\": \"7\"}," +
        "{\"colData\":\"6\", \"rowData\": \"5\", \"colorData\": \"8\"}," +
        "{\"colData\":\"6\", \"rowData\": \"6\", \"colorData\": \"8\"}" +
        "]");
}
/* jscs:enable validateQuoteMarks, maximumLineLength */
/* jshint +W109, +W101, +W098 */
