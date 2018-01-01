import exec from 'child_process';

export default function (router) {
    router.get('/job/python/getfuture', function (ctx, next) {
        var cmd = 'python C:/quantaxis/data/wind/getfuture.py';
        exec(cmd, function callback(error, stdout, stderr) {
            console.log(stdout);
            ctx.body = (stdout)
        });
    });

    router.get('/job/python/spider', function (ctx, next) {
        var cmd = 'python C:/quantaxis/data/spider/wallstreetcn/begin.py';
        exec(cmd, function callback(error, stdout, stderr) {
            console.log(stdout);
            ctx.body = (stdout)
        });
    });
}