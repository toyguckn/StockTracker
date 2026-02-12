package com.zst.backend.service;

import com.zst.backend.model.TrackingItem;
import com.zst.backend.model.User;
import com.zst.backend.model.NotificationPreference;
import com.zst.backend.service.bot.ZstTelegramBot;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    @Autowired
    private JavaMailSender mailSender;

    @Autowired
    private ZstTelegramBot telegramBot;

    public void sendStockAlert(TrackingItem item) {
        User user = item.getUser();
        String subject = "Stock Alert: " + item.getProductName();
        String text = "Good news! The product " + item.getProductName() + " (Size: " + item.getTargetSize() + ") is now in stock.\nLink: " + item.getProductUrl();

        if (user.getNotificationPreference() == NotificationPreference.EMAIL || user.getNotificationPreference() == NotificationPreference.BOTH) {
            sendEmail(user.getEmail(), subject, text);
        }

        if (user.getNotificationPreference() == NotificationPreference.TELEGRAM || user.getNotificationPreference() == NotificationPreference.BOTH) {
            if (user.getTelegramChatId() != null && !user.getTelegramChatId().isEmpty()) {
                try {
                    telegramBot.sendText(Long.parseLong(user.getTelegramChatId()), text);
                } catch (NumberFormatException e) {
                    System.err.println("Invalid Chat ID: " + user.getTelegramChatId());
                }
            }
        }
    }

    private void sendEmail(String to, String subject, String text) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        try {
            mailSender.send(message);
        } catch (Exception e) {
            System.err.println("Failed to send email: " + e.getMessage());
        }
    }
}
