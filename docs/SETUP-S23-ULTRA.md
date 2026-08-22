# S23 Ultra setup

1. Copy the complete extracted PC port to:
   `/storage/emulated/0/Download/InfinityBlade/`
2. Confirm this file exists on the phone:
   `Download/InfinityBlade/Binaries/Win64/IB2.exe`
3. Install the customized APK.
4. On first launch, let Winlator initialize its runtime and create container 1.
5. Container settings to verify:
   - Screen: 1280x720 initially
   - Graphics: Turnip/Adreno path if offered by the current upstream build
   - DX wrapper: DXVK
   - Box64: Performance
   - Audio: start with ALSA; if IB2 audio is broken, try PulseAudio
   - Drive D: Downloads
6. Close the Winlator UI and reopen the Infinity Blade II app icon. The bootstrap launcher will try the direct IB2 shortcut.

## Why this path

The provided PC port is 64-bit Windows and its UE3 configuration uses the Windows renderer and XAudio. Its cooked content contains PC Direct3D shader cache data. The Android build therefore runs the Windows executable through Wine/Box64 and translates D3D9 through DXVK rather than recompiling the UE3 game natively.
