// ng-cms
'use strict';

/*
  To publish to AWS, the following env variables must be set:
  AWS_BUCKET - sets the destination for the deployment
  AWS_SECRET_ACCESS_KEY - AWS Secret Access Key
  AWS_ACCESS_KEY_ID - AWS Access Key ID
*/

const gulp = require('gulp'),
  jade = require('gulp-jade'),
  lint = require('gulp-eslint'),
  sass = require('gulp-sass'),
  sourcemaps = require('gulp-sourcemaps'),
  runSequence = require('run-sequence'),
  browserSync = require('browser-sync'),
  rm = require('rimraf'),
  concat = require('gulp-concat'),
  uglifyjs = require('gulp-uglify'),
  uglifycss = require('gulp-uglifycss'),
  templateCache = require('gulp-angular-templatecache'),
  gulpif = require('gulp-if'),
  rename = require('gulp-rename'),
  util = require('gulp-util'),
  merge = require('merge-stream'),
  spritesmith = require('gulp.spritesmith'),
  // size = require('gulp-filesize'),
  clientLib = require('./clientLib'),
  parallelize = require('concurrent-transform');

const paths = {
  jadesrc: 'client/**/*.jade',
  sasssrc: 'client/**/*.sass',
  jssrc: 'client/**/*.js',
  fontsrc: 'node_modules/bootstrap/dist/fonts/**/*',
  fontdest: './public/fonts',
  csssrc: 'temp/**/*.css',
  spritesrc: ['client/spritesrc/*.png', 'client/spritesrc/*.gif'],
  htmlsrc: './temp/**/*.html',
  mediasrc: ['./client/assets/**/*', './src/favicon.ico'],
  destination: './public',
  temp: './temp',
  tempindex: './temp/index.html',
  manifest: './temp/rev-manifest.json',
  rev: './public/index*s',
  lib: clientLib,
  libdest: './public/lib'
};

const isProd = process.env.NODE_ENV === 'production';

gulp.task('default', function(cb) {
  runSequence(
    'build',
    'browser',
    cb
  );
});

gulp.task('build', function(cb) {
  runSequence(
    ['clean:temp', 'clean:public', 'lint'],
    ['jade', 'sass'],
    ['lib', 'assets', 'cp-index', 'fonts'],
    'sprites',
    ['bundle-templates', 'lib:bundle-js'],
    ['bundle-js', 'bundle-css'],
    ['clean:temp'],
    cb
  );
});

gulp.task('browser', function(cb) {
  runSequence(
    'browser-sync',
    ['watch:jade', 'watch:js', 'watch:sass'],
    cb
  );
});

gulp.task('clean:temp', function(cb) {
  rm(paths.temp, cb);
});

gulp.task('clean:public', function(cb) {
  rm(paths.destination, cb);
});

gulp.task('clean:aws', function(cb){
  rm(paths.aws, cb);
});

gulp.task('lint', function() {
  return gulp.src([ paths.jssrc, '!./client/assets/**/*' ])
    .pipe(lint())
    .pipe(lint.format())
    .on('error', util.log);
});

gulp.task('jade', function() {
  return gulp.src(paths.jadesrc)
    .pipe(jade({ pretty: true, doctype: 'html', locals: {isProd: isProd}}))
    .pipe(gulp.dest(paths.temp))
    .on('error', util.log);
});

gulp.task('sass', function() {
  return gulp.src(paths.sasssrc)
    .pipe(sass({includePaths: ['./client/']}).on('error', sass.logError))
    .pipe(gulp.dest(paths.temp));
});

gulp.task('lib', function() {
  return gulp.src(paths.lib.css)
    .pipe(gulp.dest(paths.libdest));
});

gulp.task('lib:bundle-js', function() {
  return gulp.src(paths.lib.js)
    .pipe(concat('vendor.js'))
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(uglifyjs())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.destination + '/lib'));
});

gulp.task('sprites', function() {
  var spriteData = gulp.src(paths.spritesrc)
    .pipe(spritesmith({
      imgName: 'sprite.png',
      cssName: 'sprite.css'
    }));

  var imgStream = spriteData.img
    .pipe(gulp.dest(paths.destination));

  var cssStream = spriteData.css
    .pipe(gulp.dest(paths.temp));

  return merge(imgStream, cssStream);
});

gulp.task('fonts', function() {
  return gulp.src(paths.fontsrc)
    .pipe(gulp.dest(paths.fontdest));
});

gulp.task('assets', function() {
  return gulp.src(paths.mediasrc)
    .pipe(gulp.dest(paths.destination + '/assets'));
});

gulp.task('bundle-js', function() {
  return gulp.src([paths.jssrc, 'temp/*.js', '!./client/assets/**/*'])
    .pipe(concat('index.js'))
    .pipe(gulpif(isProd, rename({suffix: '.min'})))
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(uglifyjs())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.destination))
    // .pipe(size())
    .on('error', util.log);
});

gulp.task('bundle-css', function() {
  return gulp.src(paths.csssrc)
    .pipe(concat('index.css'))
    .pipe(gulpif(isProd, rename({suffix: '.min'})))
    .pipe(uglifycss())
    .pipe(gulp.dest(paths.destination))
    .on('error', util.log);
});

gulp.task('cp-index', function() {
  return gulp.src(paths.tempindex)
    .pipe(gulp.dest(paths.destination));
});

gulp.task('bundle-templates', function() {
  return gulp.src(paths.htmlsrc)
    .pipe(templateCache({
      module: 'py-ferry'
    }))
    .pipe(gulp.dest(paths.temp));
});

gulp.task('watch:js', function() {
  return gulp.watch(paths.jssrc, function() {
    gulp.start('refresh:js');
  });
});

gulp.task('watch:jade', function() {
  return gulp.watch(paths.jadesrc, function() {
    gulp.start('refresh:jade');
  });
});

gulp.task('watch:sass', function() {
  return gulp.watch(paths.sasssrc, function() {
    gulp.start('refresh:sass');
  });
});

gulp.task('refresh:js', function() {
  runSequence(
    'bundle-js',
    'refresh:jade'
  );
});

gulp.task('refresh:jade', function() {
  runSequence(
    'jade',
    'bundle-templates',
    'cp-index',
    'bundle-js',
    ['reload', 'clean:temp']
  );
});

gulp.task('refresh:sass', function() {
  runSequence(
    'sprites',
    'sass',
    'bundle-css',
    ['clean:temp', 'reload']
  );
});

gulp.task('reload', function() {
  return browserSync.reload();
});

gulp.task('browser-sync', function() {
  browserSync({
    proxy: 'http://localhost:8000',
    port: 8080
  });
});
