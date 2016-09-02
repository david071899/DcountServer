from __future__ import unicode_literals

from django.db import models

from datetime import datetime

# Create your models here.
class PostData(models.Model):
  title = models.CharField(max_length=255)
  school_name = models.CharField(max_length = 255)
  forum_name = models.CharField(max_length = 255)
  forum_alias = models.CharField(max_length = 255)
  gender = models.CharField(max_length = 255)
  created_at = models.DateTimeField()
  like_count = models.IntegerField(default = 0)
  comment_count = models.IntegerField(default = 0)
  id = models.AutoField(primary_key = True)
  content = models.TextField()
  status = models.CharField(max_length = 255, default = 'online')
  updated_at = models.CharField(max_length = 255, default = 'no updated yet')

  def __unicode__(self):
    return unicode(self.title)


class ParseError(models.Model):
  id = models.AutoField(primary_key = True)
  content = models.TextField()

  def __unicode__(self):
    return unicode(self.content)  