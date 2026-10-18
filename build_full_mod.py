import base64
import os
import subprocess
import json

print("1. Reading background image...")
with open(r'C:\Users\Yjamp\.gemini\antigravity\scratch\panel_extracted\img\bg_login.jpg', 'rb') as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode('ascii')
bg_data_uri = f"data:image/jpeg;base64,{bg_base64}"
print(f"   Background data URI length: {len(bg_data_uri)}")

# JavaScript module for authentication, lock screen, animation, and in-app update
auth_code = f"""
(function() {{
    'use strict';

    var AUTH_BG_DATA_URI = "{bg_data_uri}";
    var PRIMARY_API_BASE = "https://garevynpanels.latmpx.com/youtube/panel/api/";
    var FALLBACK_API_BASE = "https://musicmod.club/youtube/panel/api/";
    var APP_SECRET = "kuropanchi950125";
    var CURRENT_TV_VERSION_CODE = 100;
    var CURRENT_TV_VERSION_NAME = "1.0.0";

    var isAuthGranted = false;
    var checkingAuth = false;

    // --- PURE JS SHA-256 ---
    function sha256(ascii) {{
        function rightRotate(value, amount) {{
            return (value >>> amount) | (value << (32 - amount));
        }}
        var mathPow = Math.pow;
        var maxWord = mathPow(2, 32);
        var lengthProperty = 'length';
        var i, j;
        var result = '';
        var words = [];
        var asciiBitLength = ascii[lengthProperty] * 8;
        var hash = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ];
        var k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ];
        for (i = 0; i < ascii[lengthProperty]; i++) {{
            var charCode = ascii.charCodeAt(i);
            words[i >> 2] |= (charCode & 0xff) << ((3 - i % 4) * 8);
        }}
        words[asciiBitLength >> 5] |= 0x80 << ((3 - (asciiBitLength >> 3) % 4) * 8);
        words[(((asciiBitLength + 64) >> 9) << 4) + 15] = asciiBitLength;

        var w = [];
        for (i = 0; i < words[lengthProperty]; i += 16) {{
            var a = hash[0];
            var b = hash[1];
            var c = hash[2];
            var d = hash[3];
            var e = hash[4];
            var f = hash[5];
            var g = hash[6];
            var h = hash[7];

            for (j = 0; j < 64; j++) {{
                if (j < 16) {{
                    w[j] = words[i + j] | 0;
                }} else {{
                    var s0 = rightRotate(w[j - 15], 7) ^ rightRotate(w[j - 15], 18) ^ (w[j - 15] >>> 3);
                    var s1 = rightRotate(w[j - 2], 17) ^ rightRotate(w[j - 2], 19) ^ (w[j - 2] >>> 10);
                    w[j] = (w[j - 16] + s0 + w[j - 7] + s1) | 0;
                }}
                var ch = (e & f) ^ (~e & g);
                var maj = (a & b) ^ (a & c) ^ (b & c);
                var temp1 = (h + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) + ch + k[j] + w[j]) | 0;
                var temp2 = ((rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) + maj) | 0;

                h = g;
                g = f;
                f = e;
                e = (d + temp1) | 0;
                d = c;
                c = b;
                b = a;
                a = (temp1 + temp2) | 0;
            }}

            hash[0] = (hash[0] + a) | 0;
            hash[1] = (hash[1] + b) | 0;
            hash[2] = (hash[2] + c) | 0;
            hash[3] = (hash[3] + d) | 0;
            hash[4] = (hash[4] + e) | 0;
            hash[5] = (hash[5] + f) | 0;
            hash[6] = (hash[6] + g) | 0;
            hash[7] = (hash[7] + h) | 0;
        }}

        for (i = 0; i < 8; i++) {{
            for (j = 3; j >= 0; j--) {{
                var bVal = (hash[i] >> (8 * j)) & 255;
                result += (bVal < 16 ? '0' : '') + bVal.toString(16);
            }}
        }}
        return result;
    }}

    // --- TIMEZONE & TOKEN HELPERS ---
    function getPanamaHourDate() {{
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var panamaTime = new Date(utc - (5 * 3600000));
        var y = panamaTime.getFullYear();
        var m = String(panamaTime.getMonth() + 1).padStart(2, '0');
        var d = String(panamaTime.getDate()).padStart(2, '0');
        var h = String(panamaTime.getHours()).padStart(2, '0');
        return y + '-' + m + '-' + d + '-' + h;
    }}

    function getDeviceMac() {{
        var mac = localStorage.getItem('ytmod_device_mac');
        if (!mac || mac.length < 12) {{
            var parts = [];
            for (var i = 0; i < 8; i++) {{
                var hex = Math.floor(Math.random() * 256).toString(16).toUpperCase();
                parts.push(hex.length === 1 ? '0' + hex : hex);
            }}
            mac = parts.join(':');
            localStorage.setItem('ytmod_device_mac', mac);
        }}
        return mac;
    }}

    function generateToken(username, mac) {{
        var hourStr = getPanamaHourDate();
        return sha256(username + mac + hourStr + APP_SECRET);
    }}

    // --- NETWORK REQUEST WITH FALLBACK ---
    function sendApiRequest(endpoint, params, callback) {{
        var qs = Object.keys(params).map(function(k) {{
            return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]);
        }}).join('&');

        function tryUrl(baseUrl, isRetry) {{
            var url = baseUrl + endpoint;
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            xhr.timeout = 12000;
            xhr.onreadystatechange = function() {{
                if (xhr.readyState === 4) {{
                    if (xhr.status >= 200 && xhr.status < 400) {{
                        try {{
                            var data = JSON.parse(xhr.responseText);
                            callback(null, data);
                        }} catch (e) {{
                            if (!isRetry) {{
                                tryUrl(FALLBACK_API_BASE, true);
                            }} else {{
                                callback(e, null);
                            }}
                        }}
                    }} else {{
                        if (!isRetry) {{
                            tryUrl(FALLBACK_API_BASE, true);
                        }} else {{
                            callback(new Error('HTTP ' + xhr.status), null);
                        }}
                    }}
                }}
            }};
            xhr.ontimeout = function() {{
                if (!isRetry) {{
                    tryUrl(FALLBACK_API_BASE, true);
                }} else {{
                    callback(new Error('Timeout'), null);
                }}
            }};
            xhr.onerror = function() {{
                if (!isRetry) {{
                    tryUrl(FALLBACK_API_BASE, true);
                }} else {{
                    callback(new Error('Network error'), null);
                }}
            }};
            xhr.send(qs);
        }}

        tryUrl(PRIMARY_API_BASE, false);
    }}

    // --- STYLES INJECTION ---
    function injectStyles() {{
        if (document.getElementById('ytmod-auth-styles')) return;
        var style = document.createElement('style');
        style.id = 'ytmod-auth-styles';
        style.textContent = `
            #ytmod-auth-screen {{
                position: fixed !important;
                inset: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 2147483647 !important;
                background-color: #080a0f !important;
                background-image: url('${{AUTH_BG_DATA_URI}}') !important;
                background-size: cover !important;
                background-position: center right !important;
                background-repeat: no-repeat !important;
                display: flex !important;
                align-items: center !important;
                justify-content: flex-start !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
                overflow: hidden !important;
                transition: opacity 0.6s ease, transform 0.6s ease !important;
            }}
            #ytmod-auth-screen::before {{
                content: '' !important;
                position: absolute !important;
                inset: 0 !important;
                background: linear-gradient(to right, rgba(8,11,18,0.97) 0%, rgba(8,11,18,0.92) 42%, rgba(8,11,18,0.35) 75%, transparent 100%) !important;
                z-index: 1 !important;
            }}
            .ytmod-content-box {{
                position: relative !important;
                z-index: 10 !important;
                margin-left: 6vw !important;
                width: 480px !important;
                max-width: 88vw !important;
                display: flex !important;
                flex-direction: column !important;
            }}
            .ytmod-badge {{
                background: rgba(225, 29, 72, 0.2) !important;
                border: 1px solid rgba(225, 29, 72, 0.5) !important;
                color: #ff476d !important;
                font-size: 13px !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 1.2px !important;
                padding: 6px 16px !important;
                border-radius: 50px !important;
                width: fit-content !important;
                margin-bottom: 14px !important;
                display: flex !important;
                align-items: center !important;
                gap: 8px !important;
                box-shadow: 0 0 15px rgba(225, 29, 72, 0.25) !important;
            }}
            .ytmod-title {{
                color: #ffffff !important;
                font-size: 36px !important;
                font-weight: 800 !important;
                line-height: 1.25 !important;
                margin: 0 0 12px 0 !important;
                text-shadow: 0 4px 20px rgba(0,0,0,0.8) !important;
            }}
            .ytmod-subtitle {{
                color: #94a3b8 !important;
                font-size: 16px !important;
                line-height: 1.5 !important;
                margin: 0 0 24px 0 !important;
            }}
            .ytmod-card {{
                background: rgba(15, 20, 32, 0.85) !important;
                backdrop-filter: blur(25px) !important;
                -webkit-backdrop-filter: blur(25px) !important;
                border: 1px solid rgba(225, 29, 72, 0.35) !important;
                border-top: 3px solid #e11d48 !important;
                border-radius: 20px !important;
                padding: 28px !important;
                box-shadow: 0 20px 50px rgba(0,0,0,0.7) !important;
            }}
            .ytmod-input-group {{
                margin-bottom: 18px !important;
                position: relative !important;
            }}
            .ytmod-input-group label {{
                display: block !important;
                color: #94a3b8 !important;
                font-size: 12px !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                margin-bottom: 8px !important;
            }}
            .ytmod-input {{
                width: 100% !important;
                background: rgba(0, 0, 0, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                padding: 14px 18px !important;
                font-size: 16px !important;
                box-sizing: border-box !important;
                outline: none !important;
                transition: all 0.2s ease !important;
            }}
            .ytmod-input:focus {{
                border-color: #e11d48 !important;
                box-shadow: 0 0 16px rgba(225, 29, 72, 0.45) !important;
                background: rgba(0, 0, 0, 0.6) !important;
            }}
            .ytmod-btn-login {{
                width: 100% !important;
                padding: 15px !important;
                background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 12px !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.8px !important;
                cursor: pointer !important;
                box-shadow: 0 6px 20px rgba(225, 29, 72, 0.4) !important;
                transition: all 0.2s ease !important;
                outline: none !important;
                margin-top: 8px !important;
            }}
            .ytmod-btn-login:hover, .ytmod-btn-login:focus {{
                transform: scale(1.02) !important;
                box-shadow: 0 0 25px rgba(225, 29, 72, 0.75), 0 0 0 2px #ffffff !important;
            }}
            .ytmod-btn-login:active {{
                transform: scale(0.98) !important;
            }}
            .ytmod-error-box {{
                display: none;
                background: rgba(225, 29, 72, 0.15) !important;
                border: 1px solid rgba(225, 29, 72, 0.4) !important;
                color: #ff6b8b !important;
                padding: 12px 16px !important;
                border-radius: 10px !important;
                font-size: 14px !important;
                margin-bottom: 16px !important;
                animation: ytmodShake 0.4s ease !important;
            }}

            /* --- ANIMATION MODAL --- */
            #ytmod-auth-modal {{
                position: fixed !important;
                inset: 0 !important;
                background: rgba(0, 0, 0, 0.82) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                z-index: 2147483648 !important;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease !important;
            }}
            #ytmod-auth-modal.ytmod-modal-active {{
                opacity: 1 !important;
                pointer-events: auto !important;
            }}
            .ytmod-modal-box {{
                background: rgba(18, 24, 38, 0.95) !important;
                border: 1px solid rgba(225, 29, 72, 0.4) !important;
                border-radius: 24px !important;
                padding: 38px 32px !important;
                width: 440px !important;
                max-width: 90vw !important;
                text-align: center !important;
                box-shadow: 0 25px 65px rgba(0,0,0,0.9) !important;
                transform: scale(0.9);
                transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            }}
            #ytmod-auth-modal.ytmod-modal-active .ytmod-modal-box {{
                transform: scale(1) !important;
            }}
            .ytmod-modal-header {{
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 12px !important;
                margin-bottom: 24px !important;
            }}
            .ytmod-modal-header h2 {{
                color: #ffffff !important;
                font-size: 24px !important;
                font-weight: 800 !important;
                margin: 0 !important;
            }}
            .ytmod-spinner {{
                width: 54px !important;
                height: 54px !important;
                border: 4px solid rgba(225, 29, 72, 0.15) !important;
                border-top: 4px solid #e11d48 !important;
                border-radius: 50% !important;
                animation: ytmodSpin 0.9s linear infinite !important;
                margin: 0 auto 24px auto !important;
            }}
            .ytmod-status-text {{
                color: #ffffff !important;
                font-size: 17px !important;
                font-weight: 600 !important;
                margin-bottom: 8px !important;
            }}
            .ytmod-substatus-text {{
                color: #94a3b8 !important;
                font-size: 14px !important;
            }}
            .ytmod-success-icon {{
                display: none;
                width: 64px !important;
                height: 64px !important;
                background: rgba(16, 185, 129, 0.15) !important;
                border: 2px solid #10b981 !important;
                border-radius: 50% !important;
                margin: 0 auto 20px auto !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 0 25px rgba(16, 185, 129, 0.4) !important;
                animation: ytmodPop 0.4s ease !important;
            }}
            .ytmod-error-icon {{
                display: none;
                width: 64px !important;
                height: 64px !important;
                background: rgba(225, 29, 72, 0.15) !important;
                border: 2px solid #e11d48 !important;
                border-radius: 50% !important;
                margin: 0 auto 20px auto !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 0 25px rgba(225, 29, 72, 0.4) !important;
            }}
            .ytmod-btn-retry {{
                display: none;
                margin-top: 20px !important;
                padding: 12px 28px !important;
                background: #e11d48 !important;
                color: #fff !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 700 !important;
                cursor: pointer !important;
                outline: none !important;
            }}
            .ytmod-btn-retry:focus {{
                box-shadow: 0 0 20px rgba(225, 29, 72, 0.8), 0 0 0 2px #fff !important;
            }}

            /* --- UPDATER MODAL --- */
            #ytmod-update-modal {{
                position: fixed !important;
                inset: 0 !important;
                background: rgba(0, 0, 0, 0.85) !important;
                backdrop-filter: blur(20px) !important;
                display: none;
                align-items: center !important;
                justify-content: center !important;
                z-index: 2147483649 !important;
            }}
            .ytmod-progress-bar-container {{
                width: 100% !important;
                height: 12px !important;
                background: rgba(255,255,255,0.1) !important;
                border-radius: 10px !important;
                overflow: hidden !important;
                margin: 20px 0 10px 0 !important;
            }}
            .ytmod-progress-fill {{
                width: 0%;
                height: 100% !important;
                background: linear-gradient(90deg, #e11d48, #ff476d) !important;
                border-radius: 10px !important;
                transition: width 0.3s ease !important;
                box-shadow: 0 0 15px rgba(225, 29, 72, 0.6) !important;
            }}

            @keyframes ytmodSpin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            @keyframes ytmodShake {{
                0%, 100% {{ transform: translateX(0); }}
                20%, 60% {{ transform: translateX(-8px); }}
                40%, 80% {{ transform: translateX(8px); }}
            }}
            @keyframes ytmodPop {{
                0% {{ transform: scale(0.6); opacity: 0; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
        `;
        document.head.appendChild(style);
    }}

    // --- DOM ELEMENTS CREATION ---
    function createAuthScreen() {{
        injectStyles();
        if (document.getElementById('ytmod-auth-screen')) return;

        var screen = document.createElement('div');
        screen.id = 'ytmod-auth-screen';
        screen.innerHTML = `
            <div class="ytmod-content-box">
                <div class="ytmod-badge">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="#ff476d"><path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 10h2v4h-2zm0 6h2v2h-2z"/></svg>
                    YOUTUBE PREMIUM
                </div>
                <h1 class="ytmod-title">Todo tu contenido sin interrupciones, sin anuncios.</h1>
                <p class="ytmod-subtitle">Acceso seguro con bloqueo de publicidad, reproducción en segundo plano y máxima resolución.</p>
                <div class="ytmod-card">
                    <div id="ytmod-error-msg" class="ytmod-error-box"></div>
                    <div class="ytmod-input-group">
                        <label for="ytmod-username-input">Usuario</label>
                        <input id="ytmod-username-input" class="ytmod-input" type="text" placeholder="Ingresa tu usuario" autocomplete="username" tabindex="1" />
                    </div>
                    <div class="ytmod-input-group">
                        <label for="ytmod-password-input">Contraseña</label>
                        <input id="ytmod-password-input" class="ytmod-input" type="password" placeholder="Ingresa tu contraseña" autocomplete="current-password" tabindex="2" />
                    </div>
                    <button id="ytmod-login-btn" class="ytmod-btn-login" tabindex="3">Iniciar Sesión</button>
                </div>
            </div>

            <!-- MODAL DE ANIMACIÓN PROFESIONAL -->
            <div id="ytmod-auth-modal">
                <div class="ytmod-modal-box">
                    <div class="ytmod-modal-header">
                        <svg width="34" height="34" viewBox="0 0 24 24" fill="#e11d48"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        <h2>YouTube Premium</h2>
                    </div>
                    <div id="ytmod-modal-spinner" class="ytmod-spinner"></div>
                    <div id="ytmod-modal-success" class="ytmod-success-icon">
                        <svg width="36" height="36" viewBox="0 0 24 24" fill="#10b981"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                    </div>
                    <div id="ytmod-modal-error" class="ytmod-error-icon">
                        <svg width="36" height="36" viewBox="0 0 24 24" fill="#e11d48"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                    </div>
                    <div id="ytmod-modal-status" class="ytmod-status-text">Autenticando usuario...</div>
                    <div id="ytmod-modal-substatus" class="ytmod-substatus-text">Validando credenciales en el servidor</div>
                    <button id="ytmod-modal-retry-btn" class="ytmod-btn-retry" tabindex="4">Reintentar</button>
                </div>
            </div>

            <!-- MODAL DE ACTUALIZACIÓN TV -->
            <div id="ytmod-update-modal">
                <div class="ytmod-modal-box">
                    <div class="ytmod-badge" style="margin: 0 auto 12px auto;">NUEVA ACTUALIZACIÓN TV</div>
                    <h2 id="ytmod-update-title" style="color: #fff; font-size: 22px; margin-bottom: 12px;">Versión disponible</h2>
                    <p id="ytmod-update-notes" style="color: #94a3b8; font-size: 14px; margin-bottom: 18px; max-height: 120px; overflow-y: auto; text-align: left; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px;"></p>
                    
                    <div id="ytmod-update-progress-area" style="display: none;">
                        <div class="ytmod-progress-bar-container">
                            <div id="ytmod-progress-fill" class="ytmod-progress-fill"></div>
                        </div>
                        <div id="ytmod-progress-text" style="color: #fff; font-size: 14px; font-weight: 600;">Descargando: 0%</div>
                    </div>

                    <div id="ytmod-update-buttons" style="display: flex; gap: 10px; margin-top: 15px; justify-content: center;">
                        <button id="ytmod-btn-update-now" class="ytmod-btn-login" style="margin:0; width: auto; padding: 12px 28px;" tabindex="5">Actualizar Ahora</button>
                        <button id="ytmod-btn-update-later" class="ytmod-btn-retry" style="display: inline-block; margin:0;" tabindex="6">Más Tarde</button>
                    </div>
                </div>
            </div>
        `;

        (document.body || document.documentElement).appendChild(screen);

        // Pre-fill user if exists
        var savedUser = localStorage.getItem('ytmod_user');
        if (savedUser) {{
            document.getElementById('ytmod-username-input').value = savedUser;
        }}

        // Bind events
        document.getElementById('ytmod-login-btn').addEventListener('click', handleManualLogin);
        document.getElementById('ytmod-password-input').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter') handleManualLogin();
        }});
        document.getElementById('ytmod-username-input').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter') document.getElementById('ytmod-password-input').focus();
        }});
        document.getElementById('ytmod-modal-retry-btn').addEventListener('click', function() {{
            hideAuthModal();
            document.getElementById('ytmod-password-input').focus();
        }});
    }}

    // --- ANIMATION CONTROLLER ---
    function showAuthModal(initialStatus, initialSubstatus) {{
        var modal = document.getElementById('ytmod-auth-modal');
        var spinner = document.getElementById('ytmod-modal-spinner');
        var successIcon = document.getElementById('ytmod-modal-success');
        var errorIcon = document.getElementById('ytmod-modal-error');
        var retryBtn = document.getElementById('ytmod-modal-retry-btn');
        var status = document.getElementById('ytmod-modal-status');
        var substatus = document.getElementById('ytmod-modal-substatus');

        if (!modal) return;
        spinner.style.display = 'block';
        successIcon.style.display = 'none';
        errorIcon.style.display = 'none';
        retryBtn.style.display = 'none';

        status.textContent = initialStatus || 'Autenticando usuario...';
        substatus.textContent = initialSubstatus || 'Validando credenciales en el servidor';
        modal.classList.add('ytmod-modal-active');
    }}

    function setModalSuccess(title, message, onComplete) {{
        var spinner = document.getElementById('ytmod-modal-spinner');
        var successIcon = document.getElementById('ytmod-modal-success');
        var status = document.getElementById('ytmod-modal-status');
        var substatus = document.getElementById('ytmod-modal-substatus');

        spinner.style.display = 'none';
        successIcon.style.display = 'flex';
        status.textContent = title || '¡Acceso Concedido!';
        substatus.textContent = message || 'Iniciando YouTube Premium...';

        setTimeout(function() {{
            hideAuthModal();
            unlockScreen();
            if (onComplete) onComplete();
        }}, 1200);
    }}

    function setModalError(title, message) {{
        var spinner = document.getElementById('ytmod-modal-spinner');
        var errorIcon = document.getElementById('ytmod-modal-error');
        var retryBtn = document.getElementById('ytmod-modal-retry-btn');
        var status = document.getElementById('ytmod-modal-status');
        var substatus = document.getElementById('ytmod-modal-substatus');

        spinner.style.display = 'none';
        errorIcon.style.display = 'flex';
        retryBtn.style.display = 'inline-block';
        retryBtn.focus();

        status.textContent = title || 'Acceso Denegado';
        substatus.textContent = message || 'Datos incorrectos o suscripción expirada.';
    }}

    function hideAuthModal() {{
        var modal = document.getElementById('ytmod-auth-modal');
        if (modal) modal.classList.remove('ytmod-modal-active');
    }}

    function unlockScreen() {{
        isAuthGranted = true;
        var screen = document.getElementById('ytmod-auth-screen');
        if (screen) {{
            screen.style.opacity = '0';
            screen.style.transform = 'scale(1.04)';
            setTimeout(function() {{
                screen.style.display = 'none';
            }}, 650);
        }}
    }}

    function lockScreen(errorMessage) {{
        isAuthGranted = false;
        var screen = document.getElementById('ytmod-auth-screen');
        if (screen) {{
            screen.style.display = 'flex';
            screen.style.opacity = '1';
            screen.style.transform = 'scale(1)';
        }}
        if (errorMessage) {{
            var errBox = document.getElementById('ytmod-error-msg');
            if (errBox) {{
                errBox.textContent = errorMessage;
                errBox.style.display = 'block';
            }}
        }}
    }}

    // --- MANUAL LOGIN HANDLER ---
    function handleManualLogin() {{
        var user = (document.getElementById('ytmod-username-input').value || '').trim();
        var pass = (document.getElementById('ytmod-password-input').value || '').trim();
        var errBox = document.getElementById('ytmod-error-msg');

        if (!user || !pass) {{
            errBox.textContent = 'Por favor ingresa usuario y contraseña.';
            errBox.style.display = 'block';
            return;
        }}
        errBox.style.display = 'none';

        var mac = getDeviceMac();
        var token = generateToken(user, mac);

        // Disparar animación bonita y profesional
        showAuthModal('Autenticando usuario...', 'Conectando con el servidor...');

        setTimeout(function() {{
            var substatus = document.getElementById('ytmod-modal-substatus');
            if (substatus) substatus.textContent = 'Validando suscripción activa...';
        }}, 400);

        sendApiRequest('player_api.php', {{
            username: user,
            password: pass,
            mac: mac,
            token: token
        }}, function(err, data) {{
            if (err) {{
                setModalError('Error de Conexión', 'No se pudo conectar con el servidor. Revisa tu internet.');
                return;
            }}

            if (data && data.user_info && Number(data.user_info.auth) === 1) {{
                localStorage.setItem('ytmod_user', user);
                localStorage.setItem('ytmod_pass', pass);
                if (data.user_info.exp_date) {{
                    localStorage.setItem('ytmod_exp_date', data.user_info.exp_date);
                }}

                var expTs = Number(data.user_info.exp_date) || 0;
                var nowTs = Math.floor(Date.now() / 1000);
                var daysLeft = expTs > nowTs ? Math.floor((expTs - nowTs) / 86400) : 0;

                setModalSuccess('¡Acceso Concedido!', 'Suscripción activa • ' + daysLeft + ' días restantes', function() {{
                    if (typeof Ro === 'function') {{
                        Ro("YouTube Premium", "¡Bienvenido, " + user + "! Suscripción activa (" + daysLeft + " días restantes)");
                    }}
                    checkForTvUpdates();
                }});
            }} else {{
                var msg = (data && data.user_info && data.user_info.message) ? data.user_info.message : 'Credenciales inválidas o cuenta inactiva';
                var cleanMsg = msg;
                if (msg.toLowerCase().indexOf('expire') !== -1) {{
                    cleanMsg = 'Tu suscripción ha expirado. Contacta a tu proveedor.';
                }} else if (msg.toLowerCase().indexOf('dispositivos') !== -1 || msg.toLowerCase().indexOf('limite') !== -1) {{
                    cleanMsg = 'Has superado el límite de dispositivos autorizados.';
                }}
                setModalError('Acceso Denegado', cleanMsg);
            }}
        }});
    }}

    // --- STEALTH CHECK ON STARTUP ---
    function performStartupCheck() {{
        var user = localStorage.getItem('ytmod_user');
        var pass = localStorage.getItem('ytmod_pass');

        if (!user || !pass) {{
            // No credentials saved, stay on lock screen
            return;
        }}

        checkingAuth = true;
        var mac = getDeviceMac();
        var token = generateToken(user, mac);

        // Show subtle checking overlay
        showAuthModal('YouTube Premium', 'Verificando suscripción activa...');

        sendApiRequest('check_api.php', {{
            username: user,
            password: pass,
            mac: mac,
            token: token
        }}, function(err, data) {{
            checkingAuth = false;
            if (data && Number(data.auth) === 1) {{
                var expTs = Number(localStorage.getItem('ytmod_exp_date')) || 0;
                var nowTs = Math.floor(Date.now() / 1000);
                var daysLeft = expTs > nowTs ? Math.floor((expTs - nowTs) / 86400) : 0;

                setModalSuccess('¡Acceso Concedido!', 'Suscripción activa (' + daysLeft + ' días restantes)', function() {{
                    if (typeof Ro === 'function') {{
                        Ro("YouTube Premium", "Suscripción activa: " + daysLeft + " días restantes");
                    }}
                    checkForTvUpdates();
                }});
            }} else {{
                hideAuthModal();
                lockScreen('Tu suscripción ha vencido o fue desactivada.');
            }}
        }});
    }}

    // --- PERIODIC STEALTH CHECK ---
    setInterval(function() {{
        if (!isAuthGranted) return;
        var user = localStorage.getItem('ytmod_user');
        var pass = localStorage.getItem('ytmod_pass');
        if (!user || !pass) {{
            lockScreen('Sesión requerida.');
            return;
        }}

        var mac = getDeviceMac();
        var token = generateToken(user, mac);

        sendApiRequest('check_api.php', {{
            username: user,
            password: pass,
            mac: mac,
            token: token
        }}, function(err, data) {{
            if (!data || Number(data.auth) !== 1) {{
                lockScreen('Tu suscripción ha expirado. Por favor renueva tu acceso.');
                // Pause any active playback
                var videos = document.querySelectorAll('video');
                for (var i = 0; i < videos.length; i++) {{
                    videos[i].pause();
                }}
            }}
        }});
    }}, 30 * 60 * 1000);

    // --- ANTI-BYPASS MONITOR ---
    setInterval(function() {{
        if (!isAuthGranted) {{
            var screen = document.getElementById('ytmod-auth-screen');
            if (!screen || screen.style.display === 'none') {{
                createAuthScreen();
                lockScreen();
            }}
            var videos = document.querySelectorAll('video');
            for (var i = 0; i < videos.length; i++) {{
                if (!videos[i].paused) videos[i].pause();
                videos[i].muted = true;
            }}
        }}
    }}, 1000);

    // --- IN-APP TV UPDATER ---
    function checkForTvUpdates() {{
        sendApiRequest('updateTV.php', {{
            v_code: CURRENT_TV_VERSION_CODE,
            v_name: CURRENT_TV_VERSION_NAME
        }}, function(err, data) {{
            if (err || !data || !data.update_available) return;

            showUpdateModal(data);
        }});
    }}

    function showUpdateModal(updateData) {{
        var modal = document.getElementById('ytmod-update-modal');
        var title = document.getElementById('ytmod-update-title');
        var notes = document.getElementById('ytmod-update-notes');
        var btnNow = document.getElementById('ytmod-btn-update-now');
        var btnLater = document.getElementById('ytmod-btn-update-later');
        var progArea = document.getElementById('ytmod-update-progress-area');
        var btnArea = document.getElementById('ytmod-update-buttons');
        var fill = document.getElementById('ytmod-progress-fill');
        var progText = document.getElementById('ytmod-progress-text');

        if (!modal) return;
        title.textContent = 'Versión ' + (updateData.version_name || '') + ' disponible';
        notes.textContent = updateData.changelog || 'Novedades y optimizaciones del sistema.';

        if (updateData.is_mandatory) {{
            btnLater.style.display = 'none';
        }} else {{
            btnLater.style.display = 'inline-block';
            btnLater.onclick = function() {{
                modal.style.display = 'none';
            }};
        }}

        btnNow.onclick = function() {{
            btnArea.style.display = 'none';
            progArea.style.display = 'block';

            // Simulate progress animation in web layer while Java streams the APK
            var progress = 0;
            var timer = setInterval(function() {{
                progress += Math.floor(Math.random() * 8) + 4;
                if (progress > 98) progress = 98;
                fill.style.width = progress + '%';
                progText.textContent = 'Descargando actualización: ' + progress + '%';
            }}, 300);

            // Call native Cobalt Starboard bridge
            if (window.h5vcc && window.h5vcc.tizentube && window.h5vcc.tizentube.InstallAppFromURL) {{
                window.h5vcc.tizentube.InstallAppFromURL(updateData.download_url);
            }} else {{
                console.warn("Native InstallAppFromURL not available in this context.");
            }}
        }};

        modal.style.display = 'flex';
        btnNow.focus();
    }}

    // --- INITIALIZATION ---
    function init() {{
        createAuthScreen();
        performStartupCheck();
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', init);
    }} else {{
        init();
    }}

}})();
"""

print("2. Reading clean user script...")
with open('userScript_clean_final.js', 'r', encoding='utf-8') as f:
    clean_js = f.read()

# Combine clean script with auth module
final_combined_js = clean_js + "\n\n/* === YOUTUBE MOD TV AUTH & UPDATER SUITE === */\n" + auth_code

output_file = 'userScript_with_auth.js'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_combined_js)

print(f"3. Saved {output_file} (length: {len(final_combined_js)} characters)")

print("4. Testing JavaScript syntax with node -c...")
res = subprocess.run(['node', '-c', output_file], capture_output=True, text=True)
if res.returncode == 0:
    print("   SUCCESS! JavaScript syntax is 100% VALID!")
else:
    print("   SYNTAX ERROR:")
    print(res.stderr[:1000])
    exit(1)

print("5. Generating C++ header third_party/blink/renderer/core/dom/youtube_mod_user_script.h...")
with open(output_file, 'rb') as f:
    data = f.read()

header_path = 'third_party/blink/renderer/core/dom/youtube_mod_user_script.h'
chunk_size = 32
lines = []
lines.append("// Generated by build_full_mod.py. Do not edit directly.\n")
lines.append("#ifndef THIRD_PARTY_BLINK_RENDERER_CORE_DOM_YOUTUBE_MOD_USER_SCRIPT_H_\n")
lines.append("#define THIRD_PARTY_BLINK_RENDERER_CORE_DOM_YOUTUBE_MOD_USER_SCRIPT_H_\n\n")
lines.append("#include <cstddef>\n\n")
lines.append("namespace blink {\n\n")
lines.append(f"static const char kYouTubeModUserScript[{len(data) + 1}] = {{\n")

for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    hex_str = ", ".join(f"0x{b:02x}" for b in chunk)
    lines.append(f"  {hex_str},\n")

lines.append("  0x00\n")
lines.append("};\n\n")
lines.append("}  // namespace blink\n\n")
lines.append("#endif  // THIRD_PARTY_BLINK_RENDERER_CORE_DOM_YOUTUBE_MOD_USER_SCRIPT_H_\n")

with open(header_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"   Successfully generated {header_path} (size: {os.path.getsize(header_path)} bytes)")
