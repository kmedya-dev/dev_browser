[app]

title = Dev Browser
package.name = dev_browser
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,css,html,js,ttf,json,spec,txt
version = 0.1
requirements = python3,pywebview[qt],watchdog,beautifulsoup4

orientation = portrait

android.permissions = INTERNET, VIBRATE

android.log_level = 2

android.api = 35
android.minapi = 21
android.ndk = 25b

# Intent filter to handle http and https URLs
android.manifest.intent_filters = 
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="http" />
        <data android:scheme="https" />
    </intent-filter>

[buildozer]

log_level = 2

# warn_on_root = 1
