from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from firebase_admin import messaging

from channel.models import ChannelScheduledMessage, ChannelMessage
from share.tasks import send_push_notification
logger = get_task_logger(__name__)

@shared_task
def send_channel_scheduled_message():
    logger.info("Running schedule Message Channel")
    try:
        now = timezone.now()
        scheduled_messages = ChannelScheduledMessage.objects.filter(
            scheduled_time__lte=now,sent=False
        )
        if not scheduled_messages.exists():
            logger.info("No scheduled message in Channel")
            return

        for scheduled_message in scheduled_messages:
            channel_message = ChannelMessage.objects.create(
                channel=scheduled_message.channel,
                sender=scheduled_message.sender,
                text=scheduled_message.text
            )
            scheduled_message.sent=True
            scheduled_message.save()
            for membership in scheduled_message.channel.memberships.all():
                notification_preference = getattr(membership.user, "notifications", None)
                if notification_preference and notification_preference.notifications_enabled:
                    send_push_notification.delay(notification_preference.device_token, f"New Message in {scheduled_message.channel.name}",
                                                 scheduled_message.text)
            logger.info(f"Group scheduled message sent {channel_message.text}")

    except Exception as e:
        logger.error(f"Error send scheduled message task: {str(e)}")

