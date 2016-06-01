/*
 Try to discover which methods have not been documented.
 This instruments the dc source so that every constructor marks
 the methods it contains comments for.  Then it constructs every
 chart type and sees whether the resulting object has methods on it
 that are not marked.

 Unfortunately this has a few false positives, and even worse, we have
 LOTS of methods which are actually internal but aren't prefixed with _,
 so it's hard to wade through the 400+ results.
*/

var mixinDocs = (function () {
    'use strict';

    var esprima = require('esprima'),
        escodegen = require('escodegen'),
        md = {};

    var DOC = md.DOC = '__doc__';

    md.insert = function (str, fragments) {
        var i, fragment, pos;

        // Sort in descending order since a fragment needs to be
        // inserted from the last one, to prevent offsetting the others.
        fragments.sort(function (a, b) {
            return b.index - a.index;
        });

        for (i = 0; i < fragments.length; i += 1) {
            fragment = fragments[i];
            pos = Math.floor(fragment.index);
            str = str.slice(0, pos) + fragment.text + str.slice(pos);
        }

        return str;
    };

    md.extractComments = function (nodeRoot) {
        var comments = [];

        function extractComments(node, parentComment, within) {
            var comment = node.leadingComments && node.leadingComments[0];
            comment = (comment && comment.type == 'Block' &&
                       comment.value[0] == '*' &&
                       comment.value[comment.value.length - 1] == '*') ?
                comment.value : undefined;

            if (parentComment && node.type == 'AssignmentExpression') {
                var left = escodegen.generate(node.left);
                comments.push({
                    value: parentComment,
                    for: left,
                    in : within,
                    range: node.range,
                    loc: node.left.loc.start.line
                });
                extractComments(node.right, comment, left);
            } else {
                for (var i in node) {
                    if (typeof (node[i]) == 'object' && node[i]) {
                        extractComments(node[i], comment || parentComment, within);
                    }
                }
            }
        }

        extractComments(nodeRoot);
        return comments;
    };

    md.instrumentSource = function (source, fileName) {
        var syntax = esprima.parse(source, {
            raw: true,
            tokens: true,
            range: true,
            loc: true,
            comment: true
        });
        syntax = escodegen.attachComments(syntax, syntax.comments, syntax.tokens);

        var comments = md.extractComments(syntax);

        var fragments = comments.map(function (c) {
            var s = +(c.value[0] == '*'),
                e = +(c.value[c.value.length - 1] == '*'),
                value = c.value.slice(s, c.value.length - e).replace(/\s+$/, ''),
                r = /(\n[ \t]+)[^ \t\n]/g,
                prefix,
                result;

            while ((result = r.exec(value))) {
                if (prefix === undefined || result[1].length < prefix.length)
                    prefix = result[1];
            }

            var aligned = value.split(prefix).join('\n').replace(/^\n+/, ''),
                assignment = c.for +"." + DOC + "=",
                doc = {
                    value: aligned,
                    for: c.for,
                    from: c.in
                };

            if (fileName) {
                doc.file = fileName;
                doc.line = c.loc;
            }

            return {
                index: c.range[1] + 1,
                text: "\n" + assignment + JSON.stringify(doc) + ";\n" // + "console.log('" + c.for + "', '" + c.in + "');"
            };
        });

        return md.insert(source, fragments);
    };

    return md;
})();

//##### dc specific code

require('d3');
var fs = require('fs'),
    dc, // ignore dc from test/env, we just want the d3/crossfilter environment
    charts = [
        'barChart',
        'boxPlot',
        'bubbleChart',
        'compositeChart',
        'dataCount',
        'dataTable',
        'geoChoroplethChart',
        'heatMap',
        'lineChart',
        'numberDisplay',
        'pieChart',
        'rowChart',
        'scatterPlot',
        'seriesChart'
    ],
    files = require("../Gruntfile").jsFiles; //fs.readdirSync(dir).map(function(f){return dir + f;});

var instrumented = [];
files.forEach(function (file) {
    console.log("Instrumenting " + file);
    var rawSource = fs.readFileSync(file, 'utf-8');
    try {
        var src = mixinDocs.instrumentSource(rawSource, file);
        instrumented.push(src);
    } catch (e) {
        console.log("  Ignoring: " + file + " (unable to parse)");
    }
});
//console.log(instrumented.join("\n"));
eval(instrumented.join("\n"));

// does not work because it is trying to instantiate the functions as charts with ('#doc')
//Object.keys(dc).filter(function(p) {
//  return typeof dc[p] == 'function';
//}).forEach(documentChart);

charts.forEach(documentChart);

function extend(obj, copy) {
    for (var k in copy) {
        obj[k] = copy[k];
    }
    return obj;
}

function documentChart(chartName) {
    var DOC = mixinDocs.DOC,
        chartFun = dc[chartName],
        chart = chartFun("#doc"),
        model = {
            name: "dc." + chartName,
            covered: [],
            missing: []
        };
    if (!chart || chart.render === undefined) return;
    Object.keys(chart).filter(function(m) {
        return typeof chart[m] == 'function' &&
               (m[0] != '_' || chart[m][mixinDocs.DOC]);
    }).forEach(function(m) {
        var method = m[0] == '_' ? m.substr(1) : m;
        if (chart[m][mixinDocs.DOC])
            model.covered.push(method);
        else {
            model.missing.push(method);
        }
    });
    model.covered.sort();
    model.missing.sort();
    model.coverage = model.covered.length / (model.covered.length + model.missing.length);

    //console.log(JSON.stringify(model));
    model.missing.forEach(function(m) {
        console.log(chartName + "." + m);
    });
}
