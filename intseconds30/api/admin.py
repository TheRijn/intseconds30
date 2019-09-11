from django.contrib import admin

from .models import Word, Card, Session

# Register your models here.

admin.site.register(Word)
admin.site.register(Card)


class PlaySessionAdmin(admin.ModelAdmin):
    readonly_fields = ('started', 'last_activity',)


admin.site.register(Session, PlaySessionAdmin)
