.PHONY: test benchmark

all: crossfilter.min.js

crossfilter.js: \
	src/identity.js \
	src/permute.js \
	src/bisect.js \
	src/heap.js \
	src/heapselect.js \
	src/insertionsort.js \
	src/quicksort.js \
	src/array.js \
	src/filter.js \
	src/null.js \
	src/zero.js \
	src/reduce.js \
	src/crossfilter.js \
	package.json \
	Makefile

%.min.js: %.js Makefile
	@rm -f $@
	node_modules/.bin/uglifyjs $< -c unsafe=true -m -o $@

%.js:
	@rm -f $@
	@echo '(function(exports){' > $@
	@echo 'crossfilter.version = "'$(shell node -p 'require("./package.json").version')'";' >> $@
	cat $(filter %.js,$^) >> $@
	@echo '})(typeof exports !== '\'undefined\'' && exports || this);' >> $@
	@chmod a-w $@

clean:
	rm -f crossfilter.js crossfilter.min.js

test: all
	@npm test

benchmark: all
	@node test/benchmark.js
