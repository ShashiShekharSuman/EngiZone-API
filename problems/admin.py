from django.contrib import admin
from .models import Tag, Question, Solution, Comment, Vote
# Register your models here.


admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(Vote)
