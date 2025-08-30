package com.example.phishzil.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.provider.Telephony
import android.util.Log
import com.example.phishzil.service.SmsBackgroundService

class SmsBroadcastReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (Telephony.Sms.Intents.SMS_RECEIVED_ACTION == intent.action) {
            val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
            for (message in messages) {
                val sender = message.originatingAddress
                val body = message.messageBody
                Log.d("PhishZil_SMS", "From: $sender, Msg: $body")

                val serviceIntent = Intent(context, SmsBackgroundService::class.java).apply {
                    putExtra("sender", sender)
                    putExtra("body", body)
                }

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    context.startForegroundService(serviceIntent)
                } else {
                    context.startService(serviceIntent)
                }
            }
        }
    }
}
