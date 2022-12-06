from lib.webhook.webhook_processor import WebhookProcessor
from lib.webhook import webhook_common

def webhook_trigger(request):
    source = webhook_common.determine_webhook_source(request)
    processor = WebhookProcessor()

    if source == "GITLAB":
        return processor.process_gitlab_webhook(request)

    if source == "GITHUB":
        return processor.process_github_webhook(request)

    # TODO: Improve the detail in the failure response
    return "400"
    