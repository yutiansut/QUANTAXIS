describe('dc.logger', function () {
    var message = 'Watch out for the bears';

    describe('logging a warning', function () {
        describe('when console.warn is defined', function () {
            beforeEach(function () {
                console.warn = function (msg) {};
                spyOn(console, 'warn');
                dc.logger.warn(message);
            });

            it('should log the message using console.warn', function () {
                expect(console.warn).toHaveBeenCalledWith(message);
            });
        });

        describe('when console.warn is not defined but console.log is', function () {
            beforeEach(function () {
                console.warn = undefined;
                spyOn(console, 'log');
                dc.logger.warn(message);
            });

            it('should log the message using console.log', function () {
                expect(console.log).toHaveBeenCalledWith(message);
            });
        });
    });

    describe('debug flag', function () {
        it('is off by default', function () {
            expect(dc.logger.enableDebugLog).toBeFalsy();
        });
    });

    describe('debug logging', function () {
        describe('when debugging is disabled', function () {
            beforeEach(function () {
                dc.logger.enableDebugLog = false;
                console.debug = function (msg) {};
                spyOn(console, 'debug');
                dc.logger.debug(message);
            });

            it('should log nothing', function () {
                expect(console.debug).not.toHaveBeenCalled();
            });
        });

        describe('when debugging is enabled', function () {
            beforeEach(function () {
                dc.logger.enableDebugLog = true;
            });

            describe('when console.debug is defined', function () {
                beforeEach(function () {
                    console.debug = function (msg) {};
                    spyOn(console, 'debug');
                    dc.logger.debug(message);
                });

                it('should log the message using console.debug', function () {
                    expect(console.debug).toHaveBeenCalledWith(message);
                });
            });

            describe('when console.debug is not defined', function () {
                beforeEach(function () {
                    console.debug = undefined;
                    spyOn(console, 'log');
                    dc.logger.debug(message);
                });

                it('should log the message using console.log', function () {
                    expect(console.log).toHaveBeenCalledWith(message);
                });
            });
        });
    });
});
