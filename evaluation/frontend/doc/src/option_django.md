---
label: Option Django
id: option_django
categorySlug:
categoryLabel: 
categoryRank: 
documentRank: 15
highlightTheme: 'solarized_dark'


Option Django
=============

Django expects html templates to be in a template directory and all other
frontend files ( js, css, images, fonts, etc ) to be located in a static
directory. 

Until now we have compiled all filed intos a build/ directory which has not
been included in version control. The idea is that the contents of the build
directory are loaded to some remote host, but are not necessary in version
control because they are built from src files.

In a django project this will typically be different. A Django project's
template and asset files are expected to be under version control, and
typically deployed directly from a central project repository.

A Django project will have no need for a build/ directory so we will have
to adapt some of the paths.

## Setup paths

In the gulp/paths.js file make the following changes:

    module.exports = {
    
        ...
        ..
        .
    
        /*
         django stuff:
         prototype is the name of this project, adapt this to
         whatever name your django module is called, for example:
         '../static/Qblog/'
         */
        jade_dest: appRoot + '../templates/prototype/',        
        dest: appRoot + '../static/prototype/',
        assets_dest: appRoot + '../static/prototype/assets/',
        scripts_output: outputRoot + '../static/prototype/scripts/',
        styleOutput: outputRoot + '../static/prototype/style/',
        
    };
    
In the gulp/tasks/jade.js change the code so it looks like this:

    var gulp = require('gulp');
    var paths = require('../paths');
    var jade = require("gulp-jade");
    
    function handleError(err) {
        console.log(err.toString());
        this.emit('end');
    }
    
    gulp.task('jade', function () {
        return gulp.src([paths.jade, paths.jade_exclude])
            .pipe(jade({
                pretty: true
            }))
            .on('error', handleError)
            // static option
            //.pipe(gulp.dest(paths.dest))
            // django option
            .pipe(gulp.dest(paths.jade_dest))
    });
    
Delete the dist folder and run the build directory again. When the build completes
you should see new static/prototype and templates/prototype directories.

Now setup the browsersync settings to work with django.

    var gulp = require('gulp');
    var browserSync = require('browser-sync').create();
    
    gulp.task('serve', ['build', 'watch'], function() {
    
          browserSync({
            online: false,            // online connectivity required?
            host: '127.0.0.1',
            port: 9000,               // different than django port
            proxy: "127.0.0.1:8000",  // default django server url + port
            startPath: "/prototype/", // open specific page
            open: '127.0.0.1'         // start the browser
          }, done);
    
        gulp.watch("templates/**/*", ['']).on('change', browserSync.reload);
        gulp.watch("static/**/*", ['']).on('change', browserSync.reload);
    })

Django modules need to have an __init__.py file, so create this:

    $ touch __init__.py
    
Depending on the type of django module you might need the one or more
of the following:

    $ touch urls.py
    $ touch models.py
    $ touch views.py
    $ touch admin.py
