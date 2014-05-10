'use strict';

// Generated on 2014-02-08 using generator-gulp-webapp 0.0.1

// Load plugins
var gulp = require('gulp');
var csso = require('gulp-csso');
var sass = require('gulp-ruby-sass');
var clean = require('gulp-clean');
var size = require('gulp-size');
var livereload = require('gulp-livereload');
var lr = require('tiny-lr');
var server = lr();

// Styles
gulp.task('styles', function () {
    return gulp.src('client/sass/app.scss')
        .pipe(sass({
          style: 'expanded',
          loadPath: ['client/bower_components']
        }))
        .pipe(csso())
        .pipe(livereload(server))
        .pipe(size())
        .pipe(gulp.dest('client/css'));
});

gulp.task('clean', function () {
    return gulp.src(['client/css'], {read: false}).pipe(clean());
});

// Build
gulp.task('build', ['styles']);

// Default task
gulp.task('default', ['clean', 'styles'], function () {
    gulp.start('build');
});

// Watch
gulp.task('watch', function () {
    // Listen on port 35729
    server.listen(35729, function (err) {
        if (err) {
            return console.error(err);
        };

        // Watch .scss files
        gulp.watch('client/sass/**/*.scss', ['styles']);
    });
});
