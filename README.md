# 💠 YouTube Mod

**YouTube Mod** is an app based on [Cobalt](https://cobalt.dev) that enhances your video viewing experience by removing ads, adding [SponsorBlock](https://sponsor.ajay.app/) support, and providing useful features like video speed control.

<details>
<summary><strong>What is Cobalt?</strong></summary>

Cobalt is a lightweight, cross-platform application container and runtime for HTML5-based apps, originally developed by Google for embedded and resource-constrained devices (like smart TVs, set-top boxes, and game consoles). It implements a subset of the W3C HTML5 standard and runs web apps with high performance on a wide range of hardware.

</details>

## ✨ Features

- 🛑 **Ad Blocker**: Enjoy your favourite streaming website without interruptions from ads.
- ❗ **SponsorBlock Support**: off by default in this app (`enableSponsorBlock: false`; a stored config from an earlier version is switched off once, `ytmod_sb_default_off`).
- ⏭️ **Video Speed Control**: Adjust playback speed to your preference.
- 🔺 **[DeArrow](https://dearrow.ajay.app/) Support**: Remove clickbait and misleading video titles.

## ❔ How to Install

1. Sideload or install the APK on your Android TV / Android device.
2. Open the app and enjoy an enhanced streaming experience!

## 📦 Package, name, icon and signing

- Package `com.io.kuromusic.garevyndev` (`manifest_package` in `cobalt/android/BUILD.gn`), shown as **YouTube Mod**, with the YouTube logo on white as icon and TV banner (`cobalt/shell/android/java/res/`). The login shows the YouTube logo and **Premium** in YouTube's font (YTSans, loaded by the YouTube TV page).
- Signing: the build signs with the owner's key when the repository secret `FIRMA_KEY` holds the Android Studio keystore (`.jks`) **in base64**, with `FIRMA_PASSWORD` (store password), `FIRMA_ALIAS` (key alias; if missing, the first private key) and `FIRMA_KEY_PASSWORD` (if different from the store password). In PowerShell: `[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\ruta\firma.jks")) | Set-Clipboard`, then paste it as the secret's value. Without a valid keystore the build says so in its log and signs with a temporary key (updates then do not install over it). `.github/workflows/firma_check.yaml` (run by hand) tells what `FIRMA_KEY` holds without printing it.

## 🧭 Menu and settings

The last block of `dist/userScript.js` wraps TizenTube's `JSON.parse`: in YouTube's settings and side menu it removes **Obtener YouTube Premium** and the entry of TizenTube's own settings (named "YouTube Premium" here: its settings still apply with their values), and puts **Shorts** right under **Principal**.

## 🛡️ Play Protect and the fixed key (Firma fija)

Without a fixed signing key every build is signed by a new `CN=Android Debug` certificate, which Play Protect has never seen; with the YouTube name and logo it can block the install ("Se bloqueó la app para proteger tu dispositivo"). The target SDK (36) has nothing to do with it.

The fixed key goes in the repository secret `ANDROID_KEYSTORE_B64`: a keystore in base64 whose key has alias `androiddebugkey` and password `android` (store and key), the values `cobalt/android/BUILD.gn` signs with. Created on Windows with Android Studio's `keytool`:

```powershell
& "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" -genkeypair -keystore "$env:USERPROFILE\youtubemod.keystore" -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -storetype pkcs12 -dname "CN=Garevyn Dev, O=KuroMusic, C=PA"
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$env:USERPROFILE\youtubemod.keystore")) | Set-Clipboard
```

Then *Settings → Secrets and variables → Actions → New repository secret*, name `ANDROID_KEYSTORE_B64`, value pasted. Keep `youtubemod.keystore` safe: an APK signed with another key never installs over this one. `firma_check.yaml` (run by hand) says in a minute whether the secret opens; the build checks it before compiling and stops with a clear message if it does not. Every build then has the same signature, so updates install over the app; Play Protect may still warn while the key is new, and the owner can allow the install on the TV (Play Store → Play Protect → turn off *Analizar apps con Play Protect*).

## 🔐 Panel login, verification and updates

`dist/userScript.js` is part of the APK: `tools/ytmod/embed_user_script.py` turns it, with the login images in `dist/login/`, into `third_party/blink/renderer/core/dom/youtube_mod_user_script.h`, and Cobalt runs it when YouTube loads (`third_party/blink/renderer/core/dom/document.cc`). The app downloads nothing from GitHub or jsDelivr, so a change pushed here only reaches TVs with a new APK. The build regenerates the header before compiling; locally, run the script after editing either folder (`--check` tells whether the header is up to date). APKs 2.0.2 and older still load `dist/userScript.js` from jsDelivr.

The script runs only in YouTube's page, not in Cobalt's native splash screen (`h5vcc-embedded://splash.html`) or in iframes. YouTube TV's page has a CSP (styles need its nonce) and requires Trusted Types, so the login never uses `innerHTML` or a plain `<style>`: its styles are a constructed stylesheet (`adoptedStyleSheets`) and the screen is built with `createElement`. Before this, the login only appeared in the splash, vanished when Cobalt switched to YouTube, and the remote stayed locked on YouTube's *Comenzar* screen.

Its first part is the access lock, the same as TizenTube Roku's:

- **Login first**: the login box is the first thing on screen, with the same background and logo as the Roku app (`dist/login/`), *Usuario*, *Contraseña*, *ENTRAR* and the device ID as the panel stores it. YouTube stays hidden, paused and without remote keys until the panel (`api/player_api.php`) accepts the user. OK on a field opens the login's own on-screen keyboard (letters, numbers, symbols, *Mayús*, *Espacio*, *Borrar*, *Listo*); *Listo* moves to the next field and Back closes it. The remote's number keys and a physical keyboard also type. Back on the login leaves the app. The password box has an **eye** at its end (SVG, no image): Right from *Contraseña* moves to it, OK shows or hides the password, Left goes back; it is crossed out while the password is hidden.
- **Saved session**: the box still shows and validates the saved user again (focus on *ENTRAR*); a network error leaves it there to retry.
- **Token**: `sha256(user + mac + hour in America/Panama + secret)`. If the TV clock is off, it retries once with the panel's own time and keeps the difference.
- **Verification** every 30 minutes (`api/check_api.php`). If it says no, `player_api.php` gives the reason; only a real refusal goes back to the login (no network keeps the session).
- **Expiry notice** (`api/check_days.php`) from 3 days left, and **updates** (`api/updateTV.php`): the app downloads the new APK with its own progress bar and opens the Android installer. A version marked mandatory or obsolete cannot be postponed.
- Login network or server errors are reported to `api/log_error.php` (`LOGIN_RED`, `LOGIN_RESPUESTA`).

The version sent to the panel is the installed APK's (`version_name` in `cobalt/android/BUILD.gn`, e.g. `2.0.4`, code `204`: its digits). To publish an update, raise `version_code`/`version_name` in `BUILD.gn` (keep each part below 10), build it, and register that same code in the panel.
