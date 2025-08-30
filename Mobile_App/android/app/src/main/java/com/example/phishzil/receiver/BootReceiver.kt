package com.example.phishzil.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.example.phishzil.service.SmsBackgroundService

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            Log.d("PhishZil_Boot", "Device rebooted - starting service")
            val serviceIntent = Intent(context, SmsBackgroundService::class.java)
            context.startForegroundService(serviceIntent)
        }
    }
}
