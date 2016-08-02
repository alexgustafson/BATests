---
label: Option Wiredep
id: option_wiredep
categorySlug:
categoryLabel: 
categoryRank: 
documentRank: 11
highlightTheme: 'solarized_dark'


Option Wiredep
==============

Wiredep is a node module that will automatically add references to js, css, 
sass and less files from packages imported via bower.

We will add a wiredep watcher that will watch the bower.json file for 
changes and then add the appropriate links.

## Install Dependencies

From the root directory issue the following commands:

    $ npm install bower --save-dev
    $ npm install wiredep --save-dev
    
    $ bower init
    
## Add Wiredep Placeholders
  
In the src/jade/index.jade file add the css and js placeholder. Css placeholders
go in the head, js placeholders at the end of the body.

    doctype html
    html(lang="en")
      head
        title= pageTitle
        script(type='text/javascript').
          if (foo) {
            bar(1 + 5)
          }
    
        // bower:css
        // endbower
    
      body
        h1 Jade - node template engine
        #container.col
          p.
            Jade is a terse and simple
            templating language with a
            strong focus on performance
            and powerful features..
    
        // bower:js
        // endbower

For bower dependencies that use sass ( susy or foundation for example ) wiredep
will automatically add those import statements to your sass style as well.
Just add the sass placeholders in your src/scss/main.scss file.


    // bower:scss
    // endbower
    
    body {
      background-color: dimgrey;
    
      h3 {
        color: white;
      }
    }
    
add the wiredep paths to the gulp/paths.js file:

    //wiredep stuff
    bowerDirectory: "bower_components",
    bowerJson: 'bower.json',
    wiredep_jade_output: appRoot + 'jade/',
    wiredep_scss_output: appRoot + 'scss/',
    wiredep_sass_output: appRoot + 'sass/',
    
create a file for your wiredep task definitions at gulp/tasks/wiredep.js:

    var paths = require('../paths');
    var gulp = require('gulp');
    var wiredep = require('wiredep').stream;
    
    var overrides = {
        // non standard package paths can be fixed here
    }
    
    
    gulp.task('wiredep-jade', function () {
        return gulp.src(paths.jade)
            .pipe(wiredep({
                directory: paths.bowerDirectory,
                ignorePath: /^(\.\.\/)*\.\./,
                overrides: overrides
            })).pipe(gulp.dest(paths.wiredep_jade_output));
    
    });
    
    
    gulp.task('wiredep-scss', function () {
        return gulp.src(paths.scss)
            .pipe(wiredep({
                directory: paths.bowerDirectory,
                overrides: overrides
            })).pipe(gulp.dest(paths.wiredep_scss_output));
    
    });
    
    gulp.task('wiredep', ['wiredep-jade','wiredep-scss']);
    
Add wiredep tasks to the build and watch tasks.

gulp/tasks/build.js:

    var gulp = require('gulp');
    var runSequence = require('run-sequence');
    
    gulp.task('build', function() {
        runSequence('wiredep', ['jade', 'scss', 'assets', 'scripts']);
    });

gulp/tasks/watch.js:

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
            gulp.watch(paths.bowerJson, ['wiredep']).on('change', reportChange);
        }
    );

test it out by adding a bower package and running the gulp build command:

    $ bower install foundation --save
    $ gulp build
    
the --save option tells bower to write the installed package to the bower.json
file. Bower will also download any dependencies that the installed package might
rely on. The gulp build task will trigger the wiredep task which looks in the bower.json 
file for packages and links the appropriate file.

Check your index.jade file and the main.scss file, you should see the 
new referenced files within the bower placeholders.

Test the watch tasks. In one console run the watcher:

    $ gulp watch
    
In another console run the bower commands:

    $ bower uninstall foundation --save
    
The bower placeholders should now be empty again. 
