/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2016, Joyent, Inc.
 */

module.exports = {
	getPass: getPass
};

const mod_tty = require('tty');
const mod_fs = require('fs');
const mod_assert = require('assert-plus');

var BACKSPACE = String.fromCharCode(127);
var CTRLC = '\u0003';
var CTRLD = '\u0004';

function getPass(opts, cb) {
	if (typeof (opts) === 'function' && cb === undefined) {
		cb = opts;
		opts = {};
	}
	mod_assert.object(opts, 'options');
	mod_assert.func(cb, 'callback');

	mod_assert.optionalString(opts.prompt, 'options.prompt');
	if (opts.prompt === undefined)
		opts.prompt = 'Password';

	openTTY(function (err, rfd, wfd, rtty, wtty) {
		if (err) {
			cb(err);
			return;
		}

		wtty.write(opts.prompt + ':');
		rtty.resume();
		rtty.setRawMode(true);
		rtty.resume();
		rtty.setEncoding('utf8');

		var pw = '';
		rtty.on('data', onData);

		function onData(data) {
			var str = data.toString('utf8');
			for (var i = 0; i < str.length; ++i) {
				var ch = str[i];
				switch (ch) {
				case '\r':
				case '\n':
				case CTRLD:
					cleanup();
					cb(null, pw);
					return;
				case CTRLC:
					cleanup();
					cb(new Error('Aborted'));
					return;
				case BACKSPACE:
					pw = pw.slice(0, pw.length - 1);
					break;
				default:
					pw += ch;
					break;
				}
			}
		}

		function cleanup() {
			wtty.write('\r\n');
			rtty.setRawMode(false);
			rtty.pause();
			rtty.removeListener('data', onData);
			if (wfd !== undefined && wfd !== rfd) {
				wtty.end();
				mod_fs.closeSync(wfd);
			}
			if (rfd !== undefined) {
				rtty.end();
				mod_fs.closeSync(rfd);
			}
		}
	});
}

function openTTY(cb) {
	mod_fs.open('/dev/tty', 'r+', function (err, rttyfd) {
		if ((err && (err.code === 'ENOENT' || err.code === 'EACCES')) ||
		    (process.version.match(/^v0[.][0-8][.]/))) {
			cb(null, undefined, undefined, process.stdin,
			    process.stdout);
			return;
		}
		var rtty = new mod_tty.ReadStream(rttyfd);
		mod_fs.open('/dev/tty', 'w+', function (err3, wttyfd) {
			var wtty = new mod_tty.WriteStream(wttyfd);
			if (err3) {
				cb(err3);
				return;
			}
			cb(null, rttyfd, wttyfd, rtty, wtty);
		});
	});
}
