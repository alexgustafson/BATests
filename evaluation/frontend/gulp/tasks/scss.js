var gulp = require('gulp');
var paths = require('../paths');
var scss = require('gulp-sass');

function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

gulp.task('scss', function() {
    return gulp.src([paths.scss])
        .pipe(scss({}))
        .on('error', handleError)
        .pipe(gulp.dest(paths.styleOutput))
});