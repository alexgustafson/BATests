var gulp = require('gulp');
var markdownDocs = require('gulp-markdown-docs');
var browserSync = require('browser-sync').create();

gulp.task('md', function () {
  return gulp.src('src/**/*.md')
    .pipe(markdownDocs('index.html', {
        yamlMeta: true,
        documentSort: 'rank'
  }))
    .pipe(gulp.dest('./documentation/'));
});

gulp.task('serve', ['md'], function () {

    // Serve files from the root of this project
    browserSync.init({
        server: {
            baseDir: "./documentation/"
        },
        injectChanges: true
    });

    gulp.watch("src/**/*.md", ['md']);
    gulp.watch("documentation/*.*", []).on('change', browserSync.reload);
});