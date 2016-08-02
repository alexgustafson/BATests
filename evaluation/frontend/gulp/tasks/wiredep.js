var paths = require('../paths');
var gulp = require('gulp');
var wiredep = require('wiredep').stream;

var overrides = {
    "fancybox": {
      "main": ["source/jquery.fancybox.css", "source/jquery.fancybox.js"]
    },
    "isotope": {
      "main": ["dist/isotope.pkgd.min.js"]
    },
    "masonry": {
      "main": ["dist/masonry.pkgd.min.js"]
    },
    "outlayer": {
      "main": [
        "item.js",
        "outlayer.js"
      ]
    },
    "foundation-datepicker": {
      "main": ["css/foundation-datepicker.scss", "js/foundation-datepicker.min.js"]
    },
    "motion-ui": {
      "main": ["src/motion-ui.scss", "dist/motion-ui.min.js"]
    },
    "semantic": {
      "main": ["dist/semantic.css", "dist/sematic.min.js"]
    },
    "concise": {
      "main": ["src/concise.scss"]
    },
    "open-iconic": {
      "main": ["font/css/open-iconic.scss"]
    }
}


gulp.task('wiredep-jade', function () {
    gulp.src(paths.jade)
        .pipe(wiredep({
            directory: paths.bowerDirectory,
            ignorePath: '../../..',
            overrides: overrides
        })).pipe(gulp.dest(paths.wiredep_jade_output));

});


gulp.task('wiredep-scss', function () {
    gulp.src(paths.scss)
        .pipe(wiredep({
            directory: paths.bowerDirectory,
            overrides: overrides
        })).pipe(gulp.dest(paths.wiredep_scss_output));

});

gulp.task('wiredep', ['wiredep-jade','wiredep-scss']);

