from django.shortcuts import render

def add_program(request):
    return render(request, 'add_program.html', {})
