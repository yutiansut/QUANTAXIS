module.exports = function (grunt) {
    'use strict';

    require('load-grunt-tasks')(grunt, {
        pattern: ['grunt-*', '!grunt-lib-phantomjs', '!grunt-template-jasmine-istanbul']
    });
    require('time-grunt')(grunt);
    var formatFileList = require('./grunt/format-file-list')(grunt);

    var config = {
        src: 'src',
        spec: 'spec',
        web: 'web',
        pkg: require('./package.json'),
        banner: grunt.file.read('./LICENSE_BANNER'),
        jsFiles: module.exports.jsFiles
    };

    grunt.initConfig({
        conf: config,

        concat: {
            options: {
                process: true,
                sourceMap: true,
                banner: '<%= conf.banner %>'
            },
            js: {
                src: '<%= conf.jsFiles %>',
                dest: '<%= conf.pkg.name %>.js'
            }
        },
        uglify: {
            jsmin: {
                options: {
                    mangle: true,
                    compress: true,
                    sourceMap: true,
                    banner: '<%= conf.banner %>'
                },
                src: '<%= conf.pkg.name %>.js',
                dest: '<%= conf.pkg.name %>.min.js'
            }
        },
        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1
            },
            main: {
                files: {
                    '<%= conf.pkg.name %>.min.css': ['<%= conf.pkg.name %>.css']
                }
            }
        },
        jscs: {
            source: {
                src: [
                    '<%= conf.src %>/**/*.js',
                    '!<%= conf.src %>/{banner,footer}.js',
                    '<%= conf.spec %>/**/*.js',
                    'Gruntfile.js',
                    'grunt/*.js',
                    '<%= conf.web %>/stock.js'],
                options: {
                    config: '.jscsrc'
                }
            }
        },
        jshint: {
            source: {
                src: [
                    '<%= conf.src %>/**/*.js',
                    '!<%= conf.src %>/{banner,footer}.js',
                    '<%= conf.spec %>/**/*.js',
                    'Gruntfile.js',
                    'grunt/*.js',
                    '<%= conf.web %>/stock.js'
                ],
                options: {
                    jshintrc: '.jshintrc'
                }
            }
        },
        watch: {
            jsdoc2md: {
                files: ['<%= conf.src %>/**/*.js'],
                tasks: ['build', 'jsdoc', 'jsdoc2md']
            },
            scripts: {
                files: ['<%= conf.src %>/**/*.js', '<%= conf.web %>/stock.js'],
                tasks: ['docs']
            },
            styles: {
                files: ['<%= conf.pkg.name %>.css'],
                tasks: ['cssmin:main', 'copy:dc-to-gh']
            },
            jasmineRunner: {
                files: ['<%= conf.spec %>/**/*.js'],
                tasks: ['jasmine:specs:build']
            },
            tests: {
                files: ['<%= conf.src %>/**/*.js', '<%= conf.spec %>/**/*.js'],
                tasks: ['test']
            },
            reload: {
                files: ['<%= conf.pkg.name %>.js',
                    '<%= conf.pkg.name %>.css',
                    '<%= conf.web %>/js/<%= conf.pkg.name %>.js',
                    '<%= conf.web %>/css/<%= conf.pkg.name %>.css',
                    '<%= conf.pkg.name %>.min.js'],
                options: {
                    livereload: true
                }
            }
        },
        connect: {
            server: {
                options: {
                    port: 8888,
                    base: '.'
                }
            }
        },
        jasmine: {
            specs: {
                options: {
                    display: 'short',
                    summary: true,
                    specs:  '<%= conf.spec %>/*-spec.js',
                    helpers: [
                        '<%= conf.web %>/js/jasmine-jsreporter.js',
                        '<%= conf.spec %>/helpers/*.js'
                    ],
                    version: '2.0.0',
                    outfile: '<%= conf.spec %>/index.html',
                    keepRunner: true
                },
                src: [
                    '<%= conf.web %>/js/d3.js',
                    '<%= conf.web %>/js/crossfilter.js',
                    '<%= conf.web %>/js/colorbrewer.js',
                    '<%= conf.pkg.name %>.js'
                ]
            },
            coverage: {
                src: '<%= jasmine.specs.src %>',
                options: {
                    specs: '<%= jasmine.specs.options.specs %>',
                    helpers: '<%= jasmine.specs.options.helpers %>',
                    version: '<%= jasmine.specs.options.version %>',
                    template: require('grunt-template-jasmine-istanbul'),
                    templateOptions: {
                        coverage: 'coverage/jasmine/coverage.json',
                        report: [
                            {
                                type: 'html',
                                options: {
                                    dir: 'coverage/jasmine'
                                }
                            }
                        ]
                    }
                }
            },
            browserify: {
                options: {
                    display: 'short',
                    summary: true,
                    specs:  '<%= conf.spec %>/*-spec.js',
                    helpers: [
                        '<%= conf.web %>/js/jasmine-jsreporter.js',
                        '<%= conf.spec %>/helpers/*.js'
                    ],
                    version: '2.0.0',
                    outfile: '<%= conf.spec %>/index-browserify.html',
                    keepRunner: true
                },
                src: [
                    'bundle.js'
                ]
            }
        },
        'saucelabs-jasmine': {
            all: {
                options: {
                    urls: ['http://localhost:8888/spec/'],
                    tunnelTimeout: 5,
                    build: process.env.TRAVIS_JOB_ID,
                    concurrency: 3,
                    browsers: [
                        {
                            browserName: 'firefox',
                            version: '43.0',
                            platform: 'Linux'
                        },
                        {
                            browserName: 'safari',
                            version: '9.0',
                            platform: 'OS X 10.11'
                        },
                        {
                            browserName: 'internet explorer',
                            version: '11.0',
                            platform: 'Windows 10'
                        },
                        {
                            browserName: 'MicrosoftEdge',
                            version: '20.10240',
                            platform: 'Windows 10'
                        }
                    ],
                    testname: '<%= conf.pkg.name %>.js'
                }
            }
        },
        jsdoc: {
            dist: {
                src: ['<%= conf.src %>/**/*.js', '!<%= conf.src %>/{banner,footer}.js'],
                options: {
                    destination: 'web/docs/html',
                    template: 'node_modules/ink-docstrap/template',
                    configure: 'jsdoc.conf.json'
                }
            }
        },
        jsdoc2md: {
            dist: {
                src: 'dc.js',
                dest: 'web/docs/api-latest.md'
            }
        },
        docco: {
            options: {
                dst: '<%= conf.web %>/docs',
                basepath: '<%= conf.web %>'
            },
            howto: {
                files: [
                    {
                        src: ['<%= conf.web %>/stock.js']
                    }
                ]
            }
        },
        copy: {
            'dc-to-gh': {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= conf.pkg.name %>.css', '<%= conf.pkg.name %>.min.css'],
                        dest: '<%= conf.web %>/css/'
                    },
                    {
                        expand: true,
                        flatten: true,
                        src: [
                            '<%= conf.pkg.name %>.js',
                            '<%= conf.pkg.name %>.js.map',
                            '<%= conf.pkg.name %>.min.js',
                            '<%= conf.pkg.name %>.min.js.map',
                            'node_modules/d3/d3.js',
                            'node_modules/crossfilter/crossfilter.js',
                            'node_modules/grunt-saucelabs/examples/jasmine/lib/jasmine-jsreporter/jasmine-jsreporter.js',
                            'test/env-data.js'
                        ],
                        dest: '<%= conf.web %>/js/'
                    }
                ]
            }
        },
        fileindex: {
            'examples-listing': {
                options: {
                    format: formatFileList,
                    absolute: true,
                    title: 'Index of dc.js examples',
                    heading: 'Examples of using dc.js',
                    description: 'An attempt to present a simple example of each chart type.',
                    sourceLink: 'https://github.com/dc-js/dc.js/tree/master/<%= conf.web %>/examples'
                },
                files: [
                    {dest: '<%= conf.web %>/examples/index.html', src: ['<%= conf.web %>/examples/*.html']}
                ]
            },
            'transitions-listing': {
                options: {
                    format: formatFileList,
                    absolute: true,
                    title: 'Index of dc.js transition tests',
                    heading: 'Eyeball tests for dc.js transitions',
                    description: 'Transitions can only be tested by eye. ' +
                        'These pages automate the transitions so they can be visually verified.',
                    sourceLink: 'https://github.com/dc-js/dc.js/tree/master/<%= conf.web %>/transitions'
                },
                files: [
                    {dest: '<%= conf.web %>/transitions/index.html', src: ['<%= conf.web %>/transitions/*.html']}
                ]
            },
            'resizing-listing': {
                options: {
                    format: formatFileList,
                    absolute: true,
                    title: 'Index of dc.js resizing tests',
                    heading: 'Eyeball tests for resizing dc.js charts',
                    description: 'It\'s a lot easier to test resizing behavior by eye. ' +
                        'These pages fit the charts to the browser dynamically so it\'s easier to test.',
                    sourceLink: 'https://github.com/dc-js/dc.js/tree/master/<%= conf.web %>/resizing'
                },
                files: [
                    {dest: '<%= conf.web %>/resizing/index.html', src: ['<%= conf.web %>/resizing/*.html']}
                ]
            }
        },

        'gh-pages': {
            options: {
                base: '<%= conf.web %>',
                message: 'Synced from from master branch.'
            },
            src: ['**']
        },
        shell: {
            merge: {
                command: function (pr) {
                    return [
                        'git fetch origin',
                        'git checkout master',
                        'git reset --hard origin/master',
                        'git fetch origin',
                        'git merge --no-ff origin/pr/' + pr + ' -m \'Merge pull request #' + pr + '\''
                    ].join('&&');
                },
                options: {
                    stdout: true,
                    failOnError: true
                }
            },
            amend: {
                command: 'git commit -a --amend --no-edit',
                options: {
                    stdout: true,
                    failOnError: true
                }
            },
            hooks: {
                command: 'cp -n scripts/pre-commit.sh .git/hooks/pre-commit' +
                    ' || echo \'Cowardly refusing to overwrite your existing git pre-commit hook.\''
            }
        },
        browserify: {
            dev: {
                src: '<%= conf.pkg.name %>.js',
                dest: 'bundle.js',
                options: {
                    browserifyOptions: {
                        standalone: 'dc'
                    }
                }
            }
        }
    });

    grunt.registerTask('merge', 'Merge a github pull request.', function (pr) {
        grunt.log.writeln('Merge Github Pull Request #' + pr);
        grunt.task.run(['shell:merge:' + pr, 'test' , 'shell:amend']);
    });
    grunt.registerTask('test-stock-example', 'Test a new rendering of the stock example web page against a ' +
        'baseline rendering', function (option) {
            require('./regression/stock-regression-test.js').testStockExample(this.async(), option === 'diff');
        });
    grunt.registerTask('update-stock-example', 'Update the baseline stock example web page.', function () {
        require('./regression/stock-regression-test.js').updateStockExample(this.async());
    });
    grunt.registerTask('watch:jasmine-docs', function () {
        grunt.config('watch', {
            options: {
                interrupt: true
            },
            runner: grunt.config('watch').jasmineRunner,
            scripts: grunt.config('watch').scripts,
            styles: grunt.config('watch').styles
        });
        grunt.task.run('watch');
    });

    // task aliases
    grunt.registerTask('build', ['concat', 'uglify', 'cssmin']);
    grunt.registerTask('docs', ['build', 'copy', 'jsdoc', 'jsdoc2md', 'docco', 'fileindex']);
    grunt.registerTask('web', ['docs', 'gh-pages']);
    grunt.registerTask('server', ['docs', 'fileindex', 'jasmine:specs:build', 'connect:server', 'watch:jasmine-docs']);
    grunt.registerTask('test', ['build', 'copy', 'jasmine:specs']);
    grunt.registerTask('test-browserify', ['build', 'copy', 'browserify', 'jasmine:browserify']);
    grunt.registerTask('coverage', ['build', 'copy', 'jasmine:coverage']);
    grunt.registerTask('ci', ['test', 'jasmine:specs:build', 'connect:server', 'saucelabs-jasmine']);
    grunt.registerTask('ci-pull', ['test', 'jasmine:specs:build', 'connect:server']);
    grunt.registerTask('lint', ['jshint', 'jscs']);
    grunt.registerTask('default', ['build', 'shell:hooks']);
    grunt.registerTask('doc-debug', ['build', 'jsdoc', 'jsdoc2md', 'watch:jsdoc2md']);
};

module.exports.jsFiles = [
    'src/banner.js',   // NOTE: keep this first
    'src/core.js',
    'src/errors.js',
    'src/utils.js',
    'src/logger.js',
    'src/events.js',
    'src/filters.js',
    'src/base-mixin.js',
    'src/margin-mixin.js',
    'src/color-mixin.js',
    'src/coordinate-grid-mixin.js',
    'src/stack-mixin.js',
    'src/cap-mixin.js',
    'src/bubble-mixin.js',
    'src/pie-chart.js',
    'src/bar-chart.js',
    'src/line-chart.js',
    'src/data-count.js',
    'src/data-table.js',
    'src/data-grid.js',
    'src/bubble-chart.js',
    'src/composite-chart.js',
    'src/series-chart.js',
    'src/geo-choropleth-chart.js',
    'src/bubble-overlay.js',
    'src/row-chart.js',
    'src/legend.js',
    'src/scatter-plot.js',
    'src/number-display.js',
    'src/heatmap.js',
    'src/d3.box.js',
    'src/box-plot.js',
    'src/footer.js'  // NOTE: keep this last
];
