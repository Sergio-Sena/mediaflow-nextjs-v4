# Video Player UI Specification

This document describes the visual and structural specifications for
reproducing the video player controls observed in the reference images.
The goal is to allow developers or designers to recreate the interface
with high visual fidelity.

------------------------------------------------------------------------

# 1. Play / Pause Button

## Structure

Shape: - Circle

Size: - 44px -- 48px

## Background

Color:

    #FFFFFF

Opacity:

    90%

Example CSS:

``` css
.play-button{
width:48px;
height:48px;
border-radius:50%;
background:rgba(255,255,255,0.9);
display:flex;
align-items:center;
justify-content:center;
}
```

## Icon

Color:

    #2F2F2F

Size:

    18px – 22px

Example:

``` css
.play-button svg{
width:20px;
height:20px;
fill:#2F2F2F;
}
```

------------------------------------------------------------------------

# 2. Volume Control

The volume control has three elements:

1.  Volume icon\
2.  Track (bar)\
3.  Knob (slider handle)

## Container

Shape: - Horizontal capsule

Size:

    height: 32px
    width: 120px

Background:

    rgba(255,255,255,0.18)

Border:

    rgba(255,255,255,0.25)

Example CSS:

``` css
.volume-control{
height:32px;
width:120px;
border-radius:16px;
background:rgba(255,255,255,0.18);
display:flex;
align-items:center;
padding:0 10px;
gap:8px;
}
```

## Volume Icon

Color:

    #FFFFFF

Opacity:

    85%

Size:

    16px

## Volume Track

Track background:

    rgba(255,255,255,0.35)

Height:

    4px

Border radius:

    2px

## Volume Fill

Color:

    #FFFFFF

## Knob (Handle)

Shape: - Circle

Size:

    10px

Color:

    #FFFFFF

Glow:

    0 0 4px rgba(255,255,255,0.6)

------------------------------------------------------------------------

# 3. Video Timer

Example display:

    0:07 / 10:58

## Typography

Recommended fonts: - Inter - Roboto

Font weight:

    500

Font size:

    14px

Color:

    #FFFFFF

Opacity:

    85%

Example CSS:

``` css
.video-timer{
color:rgba(255,255,255,0.85);
font-size:14px;
font-weight:500;
}
```

------------------------------------------------------------------------

# 4. Progress Bar (Video Scrubber)

## Container

Height:

    6px

Color:

    rgba(255,255,255,0.25)

Border radius:

    3px

## Progress Indicator

Color:

    #FF3B30

Height:

    100%

## Position Knob

Shape: - Circle

Size:

    12px

Color:

    #FF3B30

Shadow:

    0 0 6px rgba(255,59,48,0.6)

Example CSS:

``` css
.progress-bar{
height:6px;
background:rgba(255,255,255,0.25);
border-radius:3px;
}

.progress{
height:100%;
background:#FF3B30;
border-radius:3px;
}
```

------------------------------------------------------------------------

# 5. Fullscreen / Expand Button

## Container

Shape: - Rounded square or circle

Size:

    40px

Background:

    rgba(0,0,0,0.45)

Backdrop blur:

    blur(6px)

Example CSS:

``` css
.fullscreen-btn{
width:40px;
height:40px;
border-radius:10px;
background:rgba(0,0,0,0.45);
backdrop-filter:blur(6px);
display:flex;
align-items:center;
justify-content:center;
}
```

## Icon

Color:

    #FFFFFF

Opacity:

    90%

Size:

    18px

------------------------------------------------------------------------

# 6. Player Layout Structure

Modern video players typically use this structure:

    VIDEO
    ↓
    OVERLAY
    ↓
    CONTROLS

Example HTML:

``` html
<div class="video-player">

<video></video>

<div class="controls">

play
volume
timer
progress
fullscreen

</div>

</div>
```

## Controls Overlay

Background gradient:

    transparent
    ↓
    rgba(0,0,0,0.6)

Example CSS:

``` css
.controls{
position:absolute;
bottom:0;
width:100%;
padding:12px;
background:linear-gradient(
transparent,
rgba(0,0,0,0.6)
);
}
```

This pattern is widely used in modern streaming platforms.

------------------------------------------------------------------------

# 7. Video as Background (Common Pattern)

Using a video as a background layer is common in:

-   Streaming platforms
-   Game interfaces
-   Landing pages
-   Hero sections

Example structure:

``` html
<div class="hero-video">

<video autoplay muted loop></video>

<div class="overlay-ui"></div>

</div>
```

Example CSS:

``` css
.hero-video video{
width:100%;
height:100%;
object-fit:cover;
}
```

------------------------------------------------------------------------

# 8. Handling Vertical Videos

Vertical videos usually use a **9:16 aspect ratio**, while desktop
screens typically use **16:9**.

This mismatch creates side bars.

## Recommended Solution

Use:

    object-fit: cover

Example:

``` css
video{
width:100%;
height:100%;
object-fit:cover;
}
```

This fills the screen without visible bars.

## Alternative

    object-fit: contain

This preserves the entire video but may add black bars.

## Hybrid Solution (Used by Social Media)

Many platforms implement:

1.  A blurred background video
2.  The vertical video centered

Structure:

    Blurred video background
    Centered vertical video

Used by:

-   TikTok
-   Instagram Reels
-   YouTube Shorts

Example visual concept:

    ██████████████████████
    ██████████████████████
    ██░░░░░VIDEO░░░░░░░██
    ██░░░░░VERTICAL░░░░██
    ██████████████████████
    ██████████████████████

The background is a blurred copy of the same video.

------------------------------------------------------------------------

# Recommended Architecture for Modern Players

    VIDEO LAYER
    BACKGROUND VIDEO (optional)
    OVERLAY GRADIENT
    CONTROLS
    TOOLTIPS
