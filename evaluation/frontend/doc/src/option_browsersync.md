---
label: Option Browsersync
id: option_browsersync
categorySlug:
categoryLabel: 
categoryRank: 
documentRank: 14
highlightTheme: 'solarized_dark'


Option Browsersync
==================

Browsersync is a node module that starts a mini local server so that you
can test your project. Browsersync can also be configured with watchers
so that changes to your code will trigger an automatic update of the page
in the browser. 

## Install Dependencies

From the root directory issue the following commands:

    $ npm install browser-sync --save-dev

## Add Gulp Serve Task

create the serve.js task file:

    $ touch gulp/tasks/serve.js
    
add the following code to the gulp/tasks/serve.js file:

    var gulp = require('gulp');
    var browserSync = require('browser-sync').create();
    
    gulp.task('serve', ['build', 'watch'], function() {
    
        // Serve files from the root of this project
        browserSync.init({
            server: {
                baseDir: "./dist/"
            },
            injectChanges: true
        });
    
        gulp.watch("dist/**/*", ['']).on('change', browserSync.reload);
    })
    
to test this run the serve task. A browser should open and any changes you 
make in any src files should trigger a browser refresh.