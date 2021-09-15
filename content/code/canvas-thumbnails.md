Title: generating video thumbnails in js
Date: 2020-08-03 03:50
Tags: javascript, canvas, firefox
Slug: canvas-thumbnail
Description: we investigate using canvas elements to generate video thumbnails in javascript

[HTMLCanvasElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement)s are amazing for all kinds of things. Paired with the [CanvasRenderingContext2D](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D)'s [drawImage](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/drawImage) method, generating video thumbnails on browsers are incredibly easy. The interface for the method is as follows:

```
void ctx.drawImage(image, dx, dy);
void ctx.drawImage(image, dx, dy, dWidth, dHeight);
void ctx.drawImage(image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
```

Here, `image` can be any [CanvasImageSource](https://developer.mozilla.org/en-US/docs/Web/API/CanvasImageSource) such as a [HTMLImageElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement) or even a [HTMLVideoElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement).

In the following example, I will be generating a thumbnail from a video file. I've posted the same example to [StackBlitz](https://stackblitz.com/edit/generate-video-file-thumbnail). The HTML here is very simple, consisting of a [HTMLInputElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement) where [type="file"](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file) to get the file from the user and a [HTMLImageElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement) where we will later be displaying the video thumbnail:

```html
<div id="app">
  <div class="row">
    <input id="input-video-file" type="file" accepts="video/webm">
  </div>
  <div class="row">
    <img id="img-thumb" alt="Thumbnail of a video">
  </div>
</div>
<style>
  .row {
    display: block;
    padding: 10px;
  }
</style>
```

Getting the file is now as simple as listening to `input-video-file`'s change event, as so:

```javascript
const fileInput = document.querySelector("#input-video-file");
fileInput.addEventListener("change", async e => {
  const [file] = e.target.files;
});
```

We should then be able to use this file in a `HTMLVideoElement` programmatically by doing the following:

```javascript
const fileUrl = URL.createObjectURL(file);
const video = document.createElement("video");
video.src = fileUrl;
```

If you've appended the `video` element to your document body, you should now be able to play to file! Drawing that same image on a canvas is now as simple as doing:

```javascript
const canvas = document.createElement("canvas");
canvas
  .getContext("2d")
  .drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
```

Optimally, you'd do this after the [loadedmetadata event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/loadedmetadata_event) has fired, after which you can seek the video to a point of your choosing. This also ensures that the preview is already rendered in the `video` element. In this example, I seek to 25% of the video:

```javascript
video.addEventListener("loadedmetadata", () => {
  // Seek the video to 25%
  video.currentTime = video.duration * 0.25;
});

video.addEventListener("seeked", () => {
  // Draw to canvas, etc.
});
```

Next, if we wanted to generate the video thumbnail on the frontend and perhaps save that as a file we'd probably use something along the lines of:

```javascript
// ...to get the raw pixel data
const { data } = context.getImageData(0, 0, video.videoWidth, video.videoHeight);

// ...to generate a blob
canvas.toBlob(blob => { /* etc */ }, "image/png");
```

However for the purpose of this demo, we want to show it inside a `HTMLImageElement`, for which we should generate a data URI using the [HTMLCanvasElement.toDataURL](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL) method as so:

```javascript
const imageUrl = canvas.toDataURL("image/png");
const img = document.querySelector("#img-thumb");
img.src = imageUrl;
```

Piecing all these parts together, we have the following function from the demo where given a video URL we're able to generate a URL to a thumbnail of said video, _seeked_ to 25%:

```javascript
async function getThumbnailForVideo(videoUrl) {
  const video = document.createElement("video");
  const canvas = document.createElement("canvas");
  video.style.display = "none";
  canvas.style.display = "none";

  // Trigger video load
  await new Promise((resolve, reject) => {
    video.addEventListener("loadedmetadata", () => {
      video.width = video.videoWidth;
      video.height = video.videoHeight;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      // Seek the video to 25%
      video.currentTime = video.duration * 0.25;
    });
    video.addEventListener("seeked", () => resolve());
    video.src = videoUrl;
  });

  // Draw the thumbnail
  canvas
    .getContext("2d")
    .drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
  const imageUrl = canvas.toDataURL("image/png");
  return imageUrl;
}
```

Finally, here's an [onsite demo]({static}/demos/canvas-thumbnail.html). I did not transpile any of the code so please use a modern browser.

## caveats

I'd like to make a careful note however that this method is not perfect as it may not work with all videos on Firefox:

> `drawImage()` will ignore all EXIF metadata in images, including the Orientation. This behavior is especially troublesome on iOS devices. You should detect the Orientation yourself and use `rotate()` to make it right.

Put simply, this means that certain mobile-device recordings may display incorrectly in the `canvas`. As such, you may want to leverage [progressive enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement) and depending on your use-case and source of the videos, decide which users will be generating their thumbnails on the client side.

## footnote

This post is based on my [self-answered question on StackOverflow](https://stackoverflow.com/questions/63029738/how-do-i-correctly-draw-a-video-thumbnail-on-a-canvas-on-all-browsers/63083581).

<aside>
  <p>I originally wanted to preface the article with something along the following lines:</p>
  <blockquote>
    You may want to generate thumbnails of a video on the client side for a variety of reasons:
    <ul>
      <li>Displaying a thumbnail preview as a user uploads a video</li>
      <li>Creating video seekbar previews as the user hovers it</li>
      <li>Reduce server load by generating video thumbnails on the client side</li>
    </ul>
    Whatever it may be, <a href="https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement">HTMLCanvasElement</a>s make it very easy!
  </blockquote>
  <p>I decided against it because I'm starting to hate website fluff, and this seems to be especially a feature of the English language where we preface everything with foreplay. Ever tried looking up nutrition or fitness tips in English vs. Dutch/German? We talk too much, man.</p>
  <p>Perhaps it's for SEO, which is perhaps why I'm including this rant, but I lean towards the vulgar explanation of lesser malice.</p>
</aside>

