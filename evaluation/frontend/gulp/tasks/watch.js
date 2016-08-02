var gulp = require('gulp');
var paths = require('../paths')

function reportChange(event) {
    console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
}

gulp.task('watch', function () {
        gulp.watch(paths.jade, ['jade', 'jade-copy']);
        gulp.watch(paths.scss, ['scss']);
        gulp.watch(paths.assets, ['assets', ]).on('change', reportChange);
        gulp.watch(paths.scripts, ['scripts', ]).on('change', reportChange);
        gulp.watch(paths.bowerJson, ['wiredep']).on('change', reportChange);
    }
);