from rds.models import Server

def servers(request):
    return {'servers': Server.objects.all()}
