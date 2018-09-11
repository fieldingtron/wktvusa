'use strict'

import gulp from 'gulp'
import del from 'del'
import runSequence from 'run-sequence'
import gulpLoadPlugins from 'gulp-load-plugins'
import { spawn } from "child_process"
import tildeImporter from 'node-sass-tilde-importer'
import htmlmin from 'gulp-htmlmin'
import replace from 'gulp-replace'
import changed from 'gulp-changed'
import imageResize from 'gulp-image-resize'
// var replace = require('gulp-replace');



const $ = gulpLoadPlugins()
const browserSync = require('browser-sync').create()
const isProduction = process.env.NODE_ENV === 'production'

const onError = (err) => {
    console.log(err)
}

let suppressHugoErrors = false;


gulp.task('replace', function () {
    gulp.src('public/*.txt')
      .pipe(replace('foo', 'bar'))
      .pipe(gulp.dest('./public'));
  });


gulp.task('server', ['build'], () => {
    gulp.start('init-watch')
    $.watch(['archetypes/**/*', 'data/**/*', 'content/**/*', 'layouts/**/*', 'static/**/*', '!static/images/slider/*', 'config.toml'], () => gulp.start('hugo'))
});


gulp.task('init-watch', () => {
    suppressHugoErrors = true;
    browserSync.init({
        server: {
            baseDir: 'public'
        },
        open: false
    })
    $.watch('src/sass/**/*.scss', () => gulp.start('sass'))
    $.watch('src/js/**/*.js', () => gulp.start('js-watch'))
    $.watch('src/images/**/*', () => gulp.start('images'))  
})

gulp.task('build', () => {
    runSequence(['sass', 'js', 'images', 'pub-delete'], 'hugo')
})


gulp.task('minify-html', () => {
    return gulp.src('public/**/*.html')
      .pipe(htmlmin({
        collapseWhitespace: true,
        minifyCSS: true,
        minifyJS: true,
        removeComments: true,
        useShortDoctype: true,
      }))
      .pipe(gulp.dest('./public'))
  })

gulp.task('hugo', (cb) => {
    let baseUrl = process.env.NODE_ENV === 'production' ? process.env.URL : process.env.DEPLOY_PRIME_URL;
    let args = baseUrl ? ['-b', baseUrl] : [];

    return spawn('hugo', args, { stdio: 'inherit' }).on('close', (code) => {
        if (suppressHugoErrors || code === 0) {
            browserSync.reload()
            cb()
            console.log("url to deploy")
            console.log("url to deploy=" + baseUrl)
        } else {
            console.log('hugo command failed.');
            cb('hugo command failed.');
        }
    })
})



gulp.task('sass', () => {
    return gulp.src([
        'src/sass/**/*.scss'
    ])
    .pipe($.plumber({ errorHandler: onError }))
    .pipe($.print())
    .pipe($.sassLint())
    .pipe($.sassLint.format())
    .pipe($.sass({ precision: 5, importer: tildeImporter }))
    .pipe($.autoprefixer(['ie >= 10', 'last 2 versions']))
    .pipe($.if(isProduction, $.cssnano({ discardUnused: false, minifyFontValues: false })))
    .pipe($.size({ gzip: true, showFiles: true }))
    .pipe(gulp.dest('static/css'))
    .pipe(browserSync.stream())
})

gulp.task('js-watch', ['js'], (cb) => {
    browserSync.reload();
    cb();
});

gulp.task('js', () => {
    return gulp.src(['src/js/**/*.js'
    ]).pipe(gulp.dest('static/js'))
})


gulp.task('images', () => {
    return gulp.src('src/images/**/*.{png,jpg,jpeg,gif,svg,webp,ico}')
        .pipe($.newer('static/images'))
        .pipe($.print())
        .pipe($.imagemin())
        .pipe(gulp.dest('static/images'));
});

gulp.task('cms-delete', () => {
    return del(['static/admin'], { dot: true })
})

gulp.task('pub-delete', () => {
    return del(['public/**', '!public'], {
      // dryRun: true,
      dot: true
    }).then(paths => {
      console.log('Files and folders deleted:\n', paths.join('\n'), '\nTotal Files Deleted: ' + paths.length + '\n');
    })
})

gulp.task('directories', function () {
    return gulp.src('*.*', {read: false})
        .pipe(gulp.dest('static/images/slider'))  
});

gulp.task('resize', () => {
    return gulp.src('content/images/*.{png,jpg,jpeg,gif,svg,webp,ico}')
    .pipe(changed('content/images'))
    .pipe(imageResize({
        width : 1024,
        height : 768,
        crop : true,
        upscale : false
      }))
      .pipe($.imagemin())
      .pipe(gulp.dest('content/images'));
});