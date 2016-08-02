var gulp = require('gulp');
var paths = require('../paths');
var copy = require('gulp-copy');

gulp.task('assets', function () {
    return gulp.src(paths.assets)
        .pipe(copy(paths.assets_dest, {
            prefix: 2
        }));
});