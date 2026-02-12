package com.zst.backend.dto;

import com.zst.backend.model.NotificationPreference;
import lombok.Data;

@Data
public class TrackingRequest {
    private String url;
    private String size;
    private String email;
    private String telegramChatId;
    private NotificationPreference preference;
}
