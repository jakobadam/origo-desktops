from async_messages.models import Message

def unread(request):
    for m in Message.objects.filter(read=False):
        m.display(request)
    return request
