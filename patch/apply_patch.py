from pathlib import Path
import re, shutil, sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: python apply_patch.py /path/to/winlator-app")
root = Path(sys.argv[1]).resolve()
app = root / "app" / "src" / "main"
if not app.exists():
    raise SystemExit("Not a Winlator Android source tree: app/src/main missing")

# Add bootstrap activity.
src = app / "java" / "com" / "winlator"
src.mkdir(parents=True, exist_ok=True)
shutil.copy2(Path(__file__).with_name("IB2BootstrapActivity.java"), src / "IB2BootstrapActivity.java")

# Rebrand default app label while retaining upstream package ID for native compatibility.
strings = app / "res" / "values" / "strings.xml"
if strings.exists():
    s = strings.read_text(encoding="utf-8")
    s2, n = re.subn(r'(<string\s+name="app_name"[^>]*>)(.*?)(</string>)',
                     r'\1Infinity Blade II\3', s, count=1, flags=re.S)
    if n:
        strings.write_text(s2, encoding="utf-8")

# Change launcher entry from MainActivity to IB2BootstrapActivity.
manifest = app / "AndroidManifest.xml"
m = manifest.read_text(encoding="utf-8")
# Add activity if absent.
if "IB2BootstrapActivity" not in m:
    insert = '''\n        <activity\n            android:name=".IB2BootstrapActivity"\n            android:exported="true"\n            android:screenOrientation="sensorLandscape">\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n        </activity>\n'''
    m = m.replace("<application", "<application", 1)
    # Insert just before </application>.
    m = m.replace("</application>", insert + "    </application>", 1)

# Remove launcher intent-filter from MainActivity only, preserving the Activity itself.
activity_pat = re.compile(r'(<activity\b[^>]*android:name="(?:com\.winlator\.)?MainActivity"[^>]*>)(.*?)(</activity>)', re.S)
match = activity_pat.search(m)
if match:
    body = match.group(2)
    body = re.sub(r'<intent-filter>\s*<action\s+android:name="android\.intent\.action\.MAIN"\s*/>\s*<category\s+android:name="android\.intent\.category\.LAUNCHER"\s*/>\s*</intent-filter>', '', body, flags=re.S)
    m = m[:match.start()] + match.group(1) + body + match.group(3) + m[match.end():]
manifest.write_text(m, encoding="utf-8")

# Bias fresh containers toward IB2-friendly defaults without changing existing containers.
container = src / "container" / "Container.java"
if container.exists():
    c = container.read_text(encoding="utf-8")
    c = re.sub(r'public static final String DEFAULT_SCREEN_SIZE\s*=\s*"[^"]+";',
               'public static final String DEFAULT_SCREEN_SIZE = "1280x720";', c)
    # DXVK is already upstream default in current sources. Keep it explicit if field exists.
    c = re.sub(r'public static final String DEFAULT_DXWRAPPER\s*=\s*"[^"]+";',
               'public static final String DEFAULT_DXWRAPPER = "dxvk";', c)
    # Prefer performance Box64 preset where the field exists.
    c = c.replace('private String box64Preset = Box86_64Preset.INTERMEDIATE;',
                  'private String box64Preset = Box86_64Preset.PERFORMANCE;')
    container.write_text(c, encoding="utf-8")

print("IB2 patch applied.")
print("Keep game files at /storage/emulated/0/Download/InfinityBlade/")
print("Build with ./gradlew assembleDebug (or Android Studio).")
