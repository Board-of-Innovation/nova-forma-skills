# README images

`build.mjs` draws the five images the README shows, and writes them into `.github/assets/`:

- `nova-forma-banner-light.svg` and `nova-forma-banner-dark.svg`: the banner with the Nova Forma logo.
- `four-steps-light.svg`, `four-steps-dark.svg` and `four-steps-narrow.svg`: the four steps, for light and dark screens and for phones.

The text in the images is drawn as outlines, so they need no web fonts.

## Run it

You need Node.js 18 or later.

```sh
cd .github/assets/src && npm ci && node build.mjs
```

It overwrites the five SVGs in `.github/assets/`. To write them somewhere else, for a comparison, give a folder: `node build.mjs /tmp/images`.

## When a step's name or result changes

The four-steps images repeat each step's name and result. When one changes, edit `STEPS` in `build.mjs`, run it again and commit the three new four-steps images. They must match the steps table in the README and the image's alt text.

## Fonts and versions

The fonts are Funnel Display (Regular), Geist (Regular) and Geist Mono (Medium), under the SIL Open Font License 1.1. They come from the `@expo-google-fonts` packages, which ship the static TTF files from Google Fonts. `opentype.js` turns their glyphs into outlines. `package.json` and `package-lock.json` pin every version exactly, so a run gives the same bytes as the committed images.

A different font file can change the outlines even when its version number is the same. The `@fontsource` packages, for example, give different Geist outlines. After a version bump or a change of package, rebuild, look at the images, and commit them if they changed.

## The logo

`nova-forma-logo-horizontal.svg` is the Nova Forma logo the banners are drawn from. Like the banners, it is not covered by the Apache License 2.0: see [NOTICE](../../../NOTICE).

This folder ships with every plugin install, because the plugin is the whole repository. Keep it small: never commit font files or `node_modules`.
