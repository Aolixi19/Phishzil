package com.example.phishzil.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat

class SmsBackgroundService : Service() {

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(1, buildNotification("Scanning incoming SMS..."))
    }

    override fun onStartCommand(intent: Intent, flags: Int, startId: Int): Int {
        val sender = intent.getStringExtra("sender")
        val body = intent.getStringExtra("body")
        Log.d("PhishZil_Service", "Processing SMS from $sender")

        // TODO: Replace with actual AI phishing check and alert logic
        if (body?.contains("http") == true) {
            Log.w("PhishZil_Detected", "Possible phishing link in SMS: $body")
            // Trigger alert to user or backend
        }

        stopSelf()
        return START_NOT_STICKY
    }

    private fun buildNotification(content: String): Notification {
        return NotificationCompat.Builder(this, "phishzil_sms_channel")
            .setContentTitle("PhishZil SMS Scanner")
            .setContentText(content)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "phishzil_sms_channel",
                "PhishZil SMS Scanner",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
