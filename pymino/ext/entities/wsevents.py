__all__ = ("EVENT_TYPES", "NOTIF_TYPES")


EVENT_TYPES = {
        "0:0": "text_message",
        "0:100": "image_message",
        "0:103": "youtube_message",
        "1:0": "strike_message",
        "2:110": "voice_message",
        "3:113": "sticker_message",
        "50:0": "share_exurl_message",
        "52:0": "vc_not_answered",
        "53:0": "vc_not_cancelled",
        "54:0": "vc_not_declined",
        "55:0": "video_chat_not_answered",
        "56:0": "video_chat_not_cancelled",
        "57:0": "video_chat_not_declined",
        "58:0": "avatar_chat_not_answered",
        "59:0": "avatar_chat_not_cancelled",
        "60:0": "avatar_chat_not_declined",
        "100:0": "delete_message",
        "101:0": "member_join",
        "102:0": "member_leave",
        "103:0": "chat_invite",
        "104:0": "chat_background_changed",
        "105:0": "chat_title_changed",
        "106:0": "chat_icon_changed",
        "107:0": "vc_start",
        "108:0": "video_chat_start",
        "109:0": "avatar_chat_start",
        "110:0": "vc_end",
        "111:0": "video_chat_end",
        "112:0": "avatar_chat_end",
        "113:0": "chat_content_changed",
        "114:0": "screen_room_start",
        "115:0": "screen_room_end",
        "116:0": "chat_host_transfered",
        "117:0": "text_message_force_removed",
        "118:0": "chat_removed_message",
        "119:0": "mod_deleted_message",
        "120:0": "chat_tip",
        "121:0": "chat_pin_announcement",
        "122:0": "vc_permission_open_to_everyone",
        "123:0": "vc_permission_invited_and_requested",
        "124:0": "vc_permission_invite_only",
        "125:0": "chat_view_only_enabled",
        "126:0": "chat_view_only_disabled",
        "127:0": "chat_unpin_announcement",
        "128:0": "chat_tipping_enabled",
        "129:0": "chat_tipping_disabled",
        "65281:0": "timestamp_message",
        "65282:0": "welcome_message",
        "65283:0": "invite_message",
    }


NOTIF_TYPES = {
    53: "member_set_you_host",
    67: "member_set_you_cohost",
    68: "member_remove_your_cohost",
}
