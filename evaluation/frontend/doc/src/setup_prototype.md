---
label: Setup Project
id: setup_prototype
categorySlug:
categoryLabel: 
categoryRank: 
documentRank: 10
highlightTheme: 'solarized_dark'

Project Setup, Step by Step
===========================

Initialize the project directory.

    $ mkdir prototype
    $ cd prototype
    $ npm init
    
accept all default

## Install Requirements

    $ npm install gulp --save-dev
    $ npm install gulp-sass --save-dev
    $ npm install gulp-jade --save-dev
    $ npm install require-dir --save-dev
    $ npm install gulp-copy --save-dev
    $ npm install run-sequence --save-dev

## Create Source Files

    $ mkdir src
    $ mkdir src/scss
    $ mkdir src/jade
    $ mkdir src/scripts
    $ mkdir src/assets
    $ touch src/scss/main.scss
    $ touch src/jade/index.jade
    $ touch src/scripts/main.js

## Initial Gulp Setup

    $ mkdir gulp
    $ mkdir gulp/tasks
    $ touch gulpfile.js
    
add this code to gulpfile.js:

    // all gulp tasks are located in the ./build/tasks directory
    // gulp configuration is in files in ./build directory
    require('require-dir')('gulp/tasks');
    
create the gulp files

    $ touch gulp/paths.js
    $ touch gulp/tasks/scss.js
    $ touch gulp/tasks/assets.js
    $ touch gulp/tasks/scripts.js
    $ touch gulp/tasks/jade.js
    $ touch gulp/tasks/build.js
    $ touch gulp/tasks/watch.js

add this code to the gulp/paths.js file:

    var path = require('path');
    
    var appRoot = 'src/';
    var outputRoot = 'dist/';
    
    module.exports = {
    
        scss: appRoot + 'scss/**/*.scss',
        jade: appRoot + 'jade/**/*.jade',
        jade_exclude: '!' + appRoot + 'jade/**/_*.jade', // dont compile jade files that begin with _
        
        assets: appRoot + 'assets/**/*',
        assets_dest: outputRoot + 'assets/',
    
        scripts: appRoot + 'scripts/**/*.js',
        scripts_output: outputRoot + 'scripts/',
    
        styleOutput: outputRoot + 'style/*.css',
    
        dest: outputRoot
    
    };
### Setup Gulp Assets Task 
   
This task is responsible for moving and processing all binary assets 
( jpegs, pngs, svgs, etc ) into the corresponding dist folders.

In the gulp/tasks/assets.js file add the following code:

    var gulp = require('gulp');
    var paths = require('../paths');
    var copy = require('gulp-copy');
    
    gulp.task('assets', function () {
        return gulp.src(paths.assets)
            .pipe(copy(paths.assets_dest, {
                prefix: 2
            }));
    });
   
### Setup Gulp Scripts Task   
 
This task is responsible for moving and processing all javascript files
into the corresponding dist folders.

In the gulp/tasks/scripts.js file add the following code:

    var gulp = require('gulp');
    var paths = require('../paths');
    var copy = require('gulp-copy');
    
    gulp.task('scripts', function () {
        return gulp.src(paths.scripts)
            .pipe(copy(paths.scripts_output, {
                prefix: 2
            }));
    });
 
### Setup Gulp Jade Task    
    
add this code to the gulp/tasks/jade.js file:

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
            .pipe(gulp.dest(paths.dest))
    });
    
add some code to the index.jade file:

    doctype html
    html(lang="en")
      head
        title= pageTitle
        script(type='text/javascript').
          if (foo) {
            bar(1 + 5)
          }
      body
        h1 Jade - node template engine
        #container.col

          p.
            Jade is a terse and simple
            templating language with a
            strong focus on performance
            and powerful features.
            
test the gulp jade command:

    $ gulp jade
    
you should now see and index.html file in the dist/ directory

### Setup Gulp Scss Task  

add this code to the scss.js file:
    
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
    
add some styles to the main.scss file in the src/scss directory

    body {
      background-color: dimgrey;
    
      h3 {
        color: white;
      }
    
    }

test the gulp scss command:

    $ gulp scss
    
### Setup Gulp Build and Watch Tasks  

Add the 'jade' and 'scss' tasks to the build task in gulp/tasks/build.js

    var gulp = require('gulp');
    var runSequence = require('run-sequence');
    
    gulp.task('build', function() {
        runSequence('jade', 'scss', 'assets', 'scripts');
    });
    
The watch function should monitor the src folder for changes and then trigger
the appropriate task for the changed file.

When changes happen in the jade directory trigger the 'jade' gulp task, when
changes happen in the scss directory trigger the 'scss' gulp task.


    var gulp = require('gulp');
    var paths = require('../paths')
    
    function reportChange(event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    }
    
    gulp.task('watch', function () {
            gulp.watch(paths.jade, ['jade']);
            gulp.watch(paths.scss, ['scss']);
            gulp.watch(paths.assets, ['assets', ]).on('change', reportChange);
            gulp.watch(paths.scripts, ['scripts', ]).on('change', reportChange);
        }
    );
    
Test it out with the watch command:

    $ gulp watch
    
Make some changes to the index.jade or main.scss and they should get recompiled
immediately.

