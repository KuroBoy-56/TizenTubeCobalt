import re
import subprocess

with open('userScript_full.js', 'r', encoding='utf-8') as f:
    code = f.read()

print(f"Original length: {len(code)}")

# 1. Remove supportTT and socialMedia from settings menu
target_support_and_social = '{name:go("settings.supportTT.title"),icon:"MONEY_HEART",value:null,options:{title:go("settings.supportTT.title"),subtitle:go("settings.supportTT.subtitle"),content:(i=[qo(go("settings.supportTT.content.1")),qo(go("settings.supportTT.content.2")),qo(go("settings.supportTT.content.3")),qo(go("settings.supportTT.content.4")),qo(go("settings.supportTT.content.5")),qo(go("settings.supportTT.content.6"))],{scrollPaneRenderer:{content:Wo(i)}})}},{name:go("settings.options.socialMedia.title"),icon:"PRIVACY_UNLISTED",value:null,options:[{name:"GitHub",link:"https://github.com/reisxd/TizenTube"},{name:"YouTube",link:"https://www.youtube.com/@tizenbrew"},{name:"Discord",link:"https://discord.gg/m2P7v8Y2qR"},{name:`Telegram (${go("settings.options.socialMedia.announcements")})`,link:"https://t.me/tizentubecobaltofficial"},{name:`Telegram (${go("settings.options.socialMedia.group")})`,link:"https://t.me/tizentubeofficial"},{name:go("settings.options.socialMedia.website"),link:"https://tizentube.6513006.xyz"},{name:"Buy Me A Coffee",link:"https://www.buymeacoffee.com/reisxd"},{name:go("settings.options.socialMedia.githubSponsors"),link:"https://github.com/sponsors/reisxd"}].map(e=>{if(!Zo[e.name]){var t=$o.qrcode(6,"H");t.addData(e.link),t.make();var i=t.createImgTag(8,8).match(/src="([^"]+)"/)[1];Zo[e.name]=i}return{name:e.name,icon:"OPEN_IN_NEW",value:null,options:{title:e.name,subtitle:e.link,content:jo([qo(go("settings.options.socialMedia.qrCodeScanMessage",{name:e.name})),Go(Zo[e.name])])}}})},'
assert target_support_and_social in code, "target_support_and_social not found"
code = code.replace(target_support_and_social, "")

# 2. Remove updater from settings menu
target_updater_setting = 'window.h5vcc&&window.h5vcc.tizentube?{name:go("settings.options.updater.title"),icon:"SYSTEM_UPDATE",value:null,menuHeader:{title:go("settings.options.updater.title"),subtitle:go("settings.options.updater.menuSubtitle")},subtitle:go("settings.options.updater.versionSubtitle",{version:window.h5vcc.tizentube.GetVersion()}),options:[Vo({title:go("settings.options.updater.options.checkForUpdates")},{icon:"SYSTEM_UPDATE"},[{customAction:{action:"CHECK_FOR_UPDATES"}}]),{name:go("settings.options.updater.options.checkForUpdatesOnStartup"),icon:"SYSTEM_UPDATE",value:"enableUpdater"}]}:null'
assert target_updater_setting in code, "target_updater_setting not found"
code = code.replace(target_updater_setting, "null")

# 3. Neuter na(e) function (updater)
idx_na = code.find('function na(e){var t=window.h5vcc.tizentube.GetVersion()')
assert idx_na != -1, "na not found"
idx_oa = code.find('function oa(e){', idx_na)
assert idx_oa != -1, "oa not found"
code = code[:idx_na] + 'function na(e){return;}' + code[idx_oa:]

# 4. Disable auto update in setTimeout
target_timeout_update = 'setTimeout(()=>{if(window.h5vcc&&window.h5vcc.tizentube&&zo("enableUpdater")){var e=Math.floor(Date.now()/1e3);zo("dontCheckUpdateUntil")>e?console.info("Skipping update check until",new Date(1e3*zo("dontCheckUpdateUntil")).toLocaleString()):na()}},2500);'
assert target_timeout_update in code, "target_timeout_update not found"
code = code.replace(target_timeout_update, "/* auto update check disabled */")

# 5. Disable default enableUpdater flag
code = code.replace('enableUpdater:!0', 'enableUpdater:!1')

# 6. Neuter UPDATE customActions in switch:
code = code.replace('case"UPDATE_REMIND_LATER":Bo("dontCheckUpdateUntil",t);break;case"UPDATE_DOWNLOAD":window.h5vcc.tizentube.InstallAppFromURL(t),Ro(go("settings.options.updater.downloading.title"),go("settings.options.updater.downloading.subtitle"));break;', 'case"UPDATE_REMIND_LATER":break;case"UPDATE_DOWNLOAD":break;')

# 7. Clear madeByText subtitle in settings modal
code = code.replace('subtitle:go("settings.ttSettings.madeByText")', 'subtitle:""')

# 8. Toasts to "YouTube Mod"
code = code.replace('Ro("TizenTube",', 'Ro("YouTube Mod",')

# 9. In translations, replace all ttSettings:
# e.g. ttSettings:{title:"...",madeByText:"...",summary:"..."} -> ttSettings:{title:"YouTube Mod",madeByText:"",summary:"YouTube Mod"}
code = re.sub(r'ttSettings:\{title:"[^"]*",madeByText:"[^"]*",summary:"[^"]*"\}', 'ttSettings:{title:"YouTube Mod",madeByText:"",summary:"YouTube Mod"}', code)

# 10. In translations, replace all welcomeMsg:
code = re.sub(r'welcomeMsg:\{title:"[^"]*",subtitle:"[^"]*"\}', 'welcomeMsg:{title:"YouTube Mod",subtitle:""}', code)

# 11. In translations, replace withTizenTube value
code = re.sub(r'withTizenTube:"([^"]*)"', lambda m: 'withTizenTube:"' + m.group(1).replace('TizenTube', 'YouTube Mod') + '"', code)

# 12. In translations, remove supportTT, updater, socialMedia blocks safely
def remove_nested_key(text, key_prefix):
    out = []
    idx = 0
    while True:
        pos = text.find(key_prefix, idx)
        if pos == -1:
            out.append(text[idx:])
            break
        start = pos
        if start > 0 and text[start-1] == ',':
            start -= 1
        out.append(text[idx:start])
        
        brace_count = 0
        end = pos + len(key_prefix) - 1
        for i in range(end, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    idx = i + 1
                    if idx < len(text) and text[idx] == ',' and text[start] != ',':
                        idx += 1
                    break
        else:
            out.append(text[pos:])
            break
    return "".join(out)

code = remove_nested_key(code, 'supportTT:{')
code = remove_nested_key(code, 'updater:{')
code = remove_nested_key(code, 'socialMedia:{')

# Clear madeByText and __contributors
code = re.sub(r'madeByText:"[^"]*"', 'madeByText:""', code)
code = re.sub(r'__contributors:\[[^\]]*\]', '__contributors:[]', code)

# Neuter remaining CHECK_FOR_UPDATES in switch
code = code.replace('case"CHECK_FOR_UPDATES":na(!0);break;', 'case"CHECK_FOR_UPDATES":break;')

# Protect withTizenTube key/call, then replace all TizenTube in user-facing strings
code = code.replace('withTizenTube', '__PROTECTED_WITH_TT__')
code = code.replace('TizenTube', 'YouTube Mod')
code = code.replace('__PROTECTED_WITH_TT__', 'withTizenTube')

with open('userScript_clean_final.js', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Final length: {len(code)}")
print("Wrote userScript_clean_final.js successfully.")

