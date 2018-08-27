# WKTVUSA website

using some boilerplate from  [Atlas, Hugo Boilerplate](https://github.com/indigotree/atlas)

## Atlas

The [Hugo](https://gohugo.io/) boilerplate we use for our projects.

**Disclaimer** - This boilerplate has been heavily integrated with [Netlify](https://www.netlify.com/), and therefore many features are specific to the Netlify platform and may not work with other hosting providers.

**Disclaimer** - Atlas is a boilerplate (starter kit) for bespoke Hugo projects. It's not a Hugo theme and cannot be placed inside the `/themes` directory. Check the [theme](#themes) docs for more information.

## Features

Atlas provides the following features out of the box:

* A set of [Gulp](/gulpfile.babel.js) tasks for SASS, Linting, ES2015, Image compression
* Environment driven `robots.txt` file (disallows robots on everything other than production)
* Base HTML templates with easy customisation/extension
* [Configuration](/netlify.toml) for Netlify deployments
* [Better defaults](#security-headers) for configuring HTTPS
* [Better redirects](#redirects) with Netlify instead of `<meta http-equiv="refresh">`
