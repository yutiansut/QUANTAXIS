/* global makeDate */
describe('dc utils', function () {
    describe('dc.printer.filters', function () {
        var printer;
        beforeEach(function () {
            printer = dc.printers.filters;
        });
        it('print simple string', function () {
            expect(printer(['a'])).toEqual('a');
        });
        it('print range', function () {
            expect(printer([[10, 30]])).toEqual('[10 -> 30]');
        });
        it('print simple string and a range', function () {
            expect(printer(['a', [10, 30]])).toEqual('a, [10 -> 30]');
        });
    });

    describe('dc.printer.filter', function () {
        var printer;
        beforeEach(function () {
            printer = dc.printers.filter;
            dc.dateFormat = d3.time.format.utc('%m/%d/%Y');
        });
        it('print simple string', function () {
            expect(printer('a')).toEqual('a');
        });
        it('print date string', function () {
            expect(printer(makeDate(2012, 1, 1))).toEqual('02/01/2012');
        });
        it('print int range', function () {
            expect(printer([10, 30])).toEqual('[10 -> 30]');
        });
        it('print float range', function () {
            expect(printer([10.124244, 30.635623])).toEqual('[10.12 -> 30.64]');
        });
        it('print date range', function () {
            expect(printer([makeDate(2012, 1, 1), makeDate(2012, 1, 15)])).toEqual('[02/01/2012 -> 02/15/2012]');
        });
        it('print single element array', function () {
            expect(printer([makeDate(2012, 1, 1)])).toEqual('02/01/2012');
        });
        it('print null', function () {
            expect(printer(null)).toEqual('');
        });
        it('print zero', function () {
            expect(printer(0)).toEqual(0);
        });
    });

    describe('dc.utils.nameToId', function () {
        it('id should be escaped properly', function () {
            expect(dc.utils.nameToId('St. John\'s')).toEqual('st_johns');
        });
    });

    describe('dc.utils.add', function () {
        var add;
        beforeEach(function () {
            add = dc.utils.add;
        });
        it('should be able to add days', function () {
            var date = add(makeDate(2012, 0, 1), 10);
            expect(date.toString()).toEqual((makeDate(2012, 0, 11)).toString());
        });
        it('should be able to add numbers', function () {
            var num = add(10, 10);
            expect(num).toEqual(20);
        });
        it('should be able to add numbers w/ %', function () {
            var num = add(10, '10%');
            expect(num).toEqual(11);
        });
        it('should be able to add negative numbers w/ %', function () {
            var num = add(-10, '10%');
            expect(num).toEqual(-9);
        });
        it('should ignore % when adding dates', function () {
            var date = add(makeDate(2012, 0, 1), '10%');
            expect(date.toString()).toEqual(makeDate(2012, 0, 11).toString());
        });
    });
    describe('dc.utils.subtract', function () {
        var subtract;
        beforeEach(function () {
            subtract = dc.utils.subtract;
        });
        it('should be able to subtract dates', function () {
            var date = subtract(makeDate(2012, 0, 11), 10);
            expect(date.toString()).toEqual((makeDate(2012, 0, 1)).toString());
        });
        it('should be able to subtract numbers', function () {
            var num = subtract(10, 10);
            expect(num).toEqual(0);
        });
        it('should be able to subtract numbers w/ %', function () {
            var num = subtract(10, '10%');
            expect(num).toEqual(9);
        });
        it('should be able to subtract negative numbers w/ %', function () {
            var num = subtract(-10, '10%');
            expect(num).toEqual(-11);
        });
        it('should ignore % when subtracting dates', function () {
            var date = subtract(makeDate(2012, 0, 11), '10%');
            expect(date.toString()).toEqual(makeDate(2012, 0, 1).toString());
        });
    });
});

