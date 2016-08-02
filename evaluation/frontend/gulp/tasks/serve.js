var gulp = require('gulp');
var browserSync = require('browser-sync').create();

gulp.task('serve', ['build', 'watch'], function() {

    browserSync.init({
        online: false,            // online connectivity required?
        host: '127.0.0.1',
        port: 9000,               // different than django port
        proxy: "127.0.0.1:8000",  // default django server url + port
        startPath: "/", // open specific page
        open: '127.0.0.1'         // start the browser
    });

    gulp.watch("templates/**/*", ['']).on('change', browserSync.reload);
    gulp.watch("static/**/*", ['']).on('change', browserSync.reload);
})