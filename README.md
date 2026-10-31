# 💠 YouTube Mod

**YouTube Mod** is an app based on [Cobalt](https://cobalt.dev) that enhances your video viewing experience by removing ads, adding [SponsorBlock](https://sponsor.ajay.app/) support, and providing useful features like video speed control.

<details>
<summary><strong>What is Cobalt?</strong></summary>

Cobalt is a lightweight, cross-platform application container and runtime for HTML5-based apps, originally developed by Google for embedded and resource-constrained devices (like smart TVs, set-top boxes, and game consoles). It implements a subset of the W3C HTML5 standard and runs web apps with high performance on a wide range of hardware.

</details>

## ✨ Features

- 🛑 **Ad Blocker**: Enjoy your favourite streaming website without interruptions from ads.
- ❗ **SponsorBlock Support**: Automatically skip sponsored segments in videos.
- ⏭️ **Video Speed Control**: Adjust playback speed to your preference.
- 🔺 **[DeArrow](https://dearrow.ajay.app/) Support**: Remove clickbait and misleading video titles.

## ❔ How to Install

1. Sideload or install the APK on your Android TV / Android device.
2. Open the app and enjoy an enhanced streaming experience!

## 🔐 Panel login, verification and updates

The app loads `dist/userScript.js` from jsDelivr when it opens (see `third_party/blink/renderer/core/dom/document.cc`), so a change to that file reaches every installed APK without building a new one. Its first part is the access lock, the same as TizenTube Roku's:

- **Login first**: the login box is the first thing on screen, with the same background and logo as the Roku app (`dist/login/`), *Usuario*, *Contraseña*, *ENTRAR* and the device ID as the panel stores it. YouTube stays hidden, paused and without remote keys until the panel (`api/player_api.php`) accepts the user. OK on a field opens the Android keyboard, *Listo* moves to the next one, and Back leaves the app.
- **Saved session**: the box still shows and validates the saved user again (focus on *ENTRAR*); a network error leaves it there to retry.
- **Token**: `sha256(user + mac + hour in America/Panama + secret)`. If the TV clock is off, it retries once with the panel's own time and keeps the difference.
- **Verification** every 30 minutes (`api/check_api.php`). If it says no, `player_api.php` gives the reason; only a real refusal goes back to the login (no network keeps the session).
- **Expiry notice** (`api/check_days.php`) from 3 days left, and **updates** (`api/updateTV.php`): the app downloads the new APK with its own progress bar and opens the Android installer. A version marked mandatory or obsolete cannot be postponed.
- Login network or server errors are reported to `api/log_error.php` (`LOGIN_RED`, `LOGIN_RESPUESTA`).

The version sent to the panel is the installed APK's (`version_name` in `cobalt/android/BUILD.gn`, e.g. `2.0.2`, code `202`: its digits). To publish an update, raise `version_code`/`version_name` in `BUILD.gn` (keep each part below 10), build it, and register that same code in the panel.
