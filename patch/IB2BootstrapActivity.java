package com.winlator;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

/**
 * Small bootstrap activity used by the IB2-focused build.
 * It leaves Winlator's runtime intact and routes normal app launches toward a
 * transient .desktop shortcut for IB2 after container 1 exists.
 */
public class IB2BootstrapActivity extends Activity {
    private static final int CONTAINER_ID = 1;
    private static final String DESKTOP =
            "[Desktop Entry]\n" +
            "Name=Infinity Blade II\n" +
            "Exec=wine D:\\\\InfinityBlade\\\\Binaries\\\\Win64\\\\IB2.exe\n" +
            "Type=Application\n" +
            "StartupNotify=true\n" +
            "Path=D:\\\\InfinityBlade\\\\Binaries\\\\Win64\n";

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        File container = new File(getFilesDir(), "imagefs/home/xuser-" + CONTAINER_ID + "/.container");
        if (!container.exists()) {
            Toast.makeText(this,
                    "First launch: initialize Winlator and create container 1. Then reopen Infinity Blade II.",
                    Toast.LENGTH_LONG).show();
            startActivity(new Intent(this, MainActivity.class));
            finish();
            return;
        }

        try {
            File dir = new File(getFilesDir(), "desktops");
            if (!dir.exists() && !dir.mkdirs()) throw new Exception("Could not create shortcut directory");
            File shortcut = new File(dir, "Infinity Blade II.desktop");
            try (FileOutputStream out = new FileOutputStream(shortcut, false)) {
                out.write(DESKTOP.getBytes(StandardCharsets.UTF_8));
            }

            Intent i = new Intent(this, XServerDisplayActivity.class);
            i.putExtra("container_id", CONTAINER_ID);
            i.putExtra("shortcut_path", shortcut.getAbsolutePath());
            i.putExtra("shortcut_name", "Infinity Blade II");
            i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(i);
            finish();
        } catch (Throwable t) {
            Toast.makeText(this, "IB2 launch setup failed: " + t.getMessage(), Toast.LENGTH_LONG).show();
            startActivity(new Intent(this, MainActivity.class));
            finish();
        }
    }
}
