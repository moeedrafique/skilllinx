from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.db.models import Q
from django.utils.text import slugify

class Banner(models.Model):
    ## for product category
    name = models.CharField(max_length=150, blank=True)
    detail = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='home_main_banners/', blank=True, null=True)
    # url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Banner Image'
        verbose_name_plural = 'Banner Images'

class Category(models.Model):
    category = models.CharField(max_length=300, default=None, null=True)
    image = models.ImageField(upload_to='course_categories/', default=None, blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.category:
            self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class CoursesManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(course_name__icontains=query) |
                         Q(duration__icontains=query) |
                         Q(details__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs

class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    course_code = models.CharField(max_length=300, default=None)
    course_name = models.CharField(max_length=300)
    duration = models.CharField(max_length=300, default=None)
    fees = models.CharField(max_length=300, default=None)
    details = RichTextUploadingField(blank=True, null=True,
        config_name='special',
    )
    objects = CoursesManager()

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.course_name:
            self.slug = slugify(self.course_name)
        super(Courses, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_code + ',  ' + str(self.category)

    class Meta:
        verbose_name = 'University Course'
        verbose_name_plural = 'University Courses'


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class CourseOffering(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('course', 'city')