module.exports = function (grunt) {
    return function (list, opts) {
        var files = list.sort().map(function (entry) {
            var f = entry.replace(/.*\//, '');
            return [f.replace('.html', '').replace(/-/g, ' '), f];
        }).filter(function (e) { return e[0] !== 'index'; });
        var rows = [];
        for (var i = 0; i < files.length; i += 5) {
            var cols = [];
            for (var j = 0; j < 5; ++j) {
                if (i + j >= files.length) {
                    break;
                }
                var file = files[i + j];
                cols.push('    <td><a href="' + file[1] + '">' + file[0] + '</a></td>');
            }
            rows.push('  <tr>\n' + cols.join('\n') + '\n<tr>');
        }
        var body = '<table class="table">\n' + rows.join('\n') + '\n</table>';
        return [
            '<html><head><title>' + opts.title + '</title>',
            '<link rel="stylesheet" type="text/css" href="../css/bootstrap.min.css"></head>',
            '<body><div class="container">',
            '<h2>' + opts.heading + '</h2>',
            '<p>' + opts.description + '</p>',
            '<p>Contributions <a href="https://github.com/dc-js/dc.js/blob/master/CONTRIBUTING.md">' + 'welcome</a>.',
            'Source <a href="' + opts.sourceLink + '">',
            'here</a>.</p>',
            body,
            '</div></body></html>'
        ].join('\n');
    };
};
