describe('dc event engine', function () {
    describe('event execution', function () {
        var engine, trigger;
        beforeEach(function () {
            engine = dc.events;
            trigger = jasmine.createSpy('trigger');
        });

        it('event can be dispatched immediately', function () {
            engine.trigger(trigger);
            expect(trigger).toHaveBeenCalled();
        });

        it('event can be dispatched with delay', function () {
            engine.trigger(trigger, 100);
            expect(trigger).not.toHaveBeenCalled();
            jasmine.clock().tick(101);
            expect(trigger).toHaveBeenCalled();
        });

        it('multiple events dispatched with delay should be throttled', function () {
            var times = 0;
            var i = 0;
            var increment = function () {
                times++;
            };

            while (i < 10) {
                engine.trigger(increment.bind(null), 10);
                i++;
            }
            jasmine.clock().tick(5);
            expect(times).toEqual(0);
            jasmine.clock().tick(5);
            expect(times).toEqual(1);
        });
        afterEach(function () {
        });
    });
});

