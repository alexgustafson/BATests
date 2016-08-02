var gulp = require('gulp');
var paths = require('../paths');
var copy = require('gulp-copy');

gulp.task('scripts', function () {
    return gulp.src(paths.scripts)
        .pipe(copy(paths.scripts_output, {
            prefix: 2
        }));
});