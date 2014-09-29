from django.dispatch import Signal

file_load = Signal(providing_args=['fileobj'])