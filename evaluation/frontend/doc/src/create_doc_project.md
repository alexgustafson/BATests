---
label: Setup Documentation Project
id: doc_howto
categorySlug:
categoryLabel: 
categoryRank: 
documentRank: 20
highlightTheme: 'solarized_dark'

How to Create the Documentation Project
=======================================

We will create a simple gulp project that will allow us to write nice Markdown based documentation. 
We will use Gulp and Browsersync to let us view edits in the browser as we are making then. 
We'll use gulp-markdown-docs to compile our markdown to html.

First let's install the requirements.

## Install Requirements

    $ mkdir doc

    $ cd doc
    
    $ mkdir src
    
    $ mkdir documentation

    $ npm init

    This utility will walk you through creating a package.json file.
    It only covers the most common items, and tries to guess sensible defaults.

    See `npm help json` for definitive documentation on these fields
    and exactly what they do.

    Use `npm install <pkg> --save` afterwards to install a package and
    save it as a dependency in the package.json file.

    Press ^C at any time to quit.
    name: (doc) frontend-doc
    version: (1.0.0)
    description: documentation of frontend 
    entry point: (index.js)
    test command:
    git repository:
    keywords:
    author:
    license: (ISC)
    About to write to path/path/path/doc/package.json:

    {
      "name": "frontend-doc",
      "version": "1.0.0",
      "description": "documentation of frontend",
      "main": "index.js",
      "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
      },
      "author": "",
      "license": "ISC"
    }

    Is this ok? (yes) yes

    $ npm install gulp --save-dev

    $ npm install --save-dev gulp-markdown-docs

    $ npm install browser-sync gulp --save-dev

## Project Structure

Some files have been generated automatically already, you need to create the others at this point by hand.
In the doc folder create the following two files:

    $ touch gulpfile.js

    $ touch .gitignore

In the src directory create a file named chapter1.md. 

The doc directory structure should look like the following:

    doc/
        documentation/
        node_modules/
        src/
            chapter1.md
        .gitignore
        gulpfile.js
        package.json


## Create gulpfile.js

    var gulp = require('gulp');
    var markdownDocs = require('gulp-markdown-docs');
    var browserSync = require('browser-sync').create();

    gulp.task('md', function () {
      return gulp.src('src/**/*.md')
        .pipe(markdownDocs('index.html', {
            yamlMeta: true,
            documentSort: 'rank'
      }))
        .pipe(gulp.dest('./documentation/'));
    });

    gulp.task('serve', ['md'], function () {

        // Serve files from the root of this project
        browserSync.init({
            server: {
                baseDir: "./documentation/"
            },
            injectChanges: true
        });

        gulp.watch("src/**/*.md", ['md']);
        gulp.watch("documentation/*.*", []).on('change', browserSync.reload);
    });

## Create Documentation

Gulp Markdown Docs looks for some yaml formated meta information at the top of each page. 

    label: [page label here]
    id: [page_id_for_anchor]