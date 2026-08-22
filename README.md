# Infinity Blade II Android Wrapper Kit

This kit customizes the open-source Winlator Android project into an Infinity Blade II-focused launcher.
It does **not** include Infinity Blade II game files. Put your own extracted Windows port in:

`/storage/emulated/0/Download/InfinityBlade/`

Expected executable:

`/storage/emulated/0/Download/InfinityBlade/Binaries/Win64/IB2.exe`

The wrapper keeps Winlator's package ID (`com.winlator`) intentionally because the upstream native code contains package-specific paths. Install this build instead of stock Winlator, not alongside it.

## Target profile

- Device: Samsung Galaxy S23 Ultra / Snapdragon 8 Gen 2 / Adreno 740
- Wine translation: Winlator / Box64
- Graphics: Turnip-compatible Vulkan path + DXVK
- Resolution: 1280x720 first-run baseline for stability
- Executable: `D:\\InfinityBlade\\Binaries\\Win64\\IB2.exe`
- Saves: Wine Documents path, matching IB2's `My Games/Infinity Blade II/SwordGame/Cloud`

## Build

1. Clone `https://github.com/brunodev85/winlator-app`.
2. From this kit, run:
   - Windows: `python patch/apply_patch.py C:\\path\\to\\winlator-app`
   - macOS/Linux: `python3 patch/apply_patch.py /path/to/winlator-app`
3. Open the patched project in Android Studio, or run `gradlew assembleDebug`.
4. Install the generated APK.
5. Copy your extracted `InfinityBlade` folder to the phone's `Download` directory.
6. First launch initializes Winlator. Create container 1 if the upstream first-run flow asks for one.
7. Subsequent launches attempt to go directly to IB2.

## Important

This is a source customization kit, not a precompiled APK. The current execution environment used to produce this kit does not contain the Android SDK/NDK or Winlator's runtime payload, so it cannot compile/sign a working Winlator-derived APK locally.
