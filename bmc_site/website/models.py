from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.db.models import Q, Count
from django.utils.text import slugify
from django_countries.fields import CountryField

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
    banner = models.ImageField(upload_to='category_banners/', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.category:
            self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def countreview(self):
        reviews = Courses.objects.select_related('course_name', 'course').filter(name=self).aggregate(count=Count('name_id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
            return cnt

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


DURATION_CHOICES = [
    ('One Week', 'One Week'),
    ('Two Weeks', 'Two Weeks'),
    ('Three Weeks', 'Three Weeks'),
    ('Four Weeks', 'Four Weeks'),
]

class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    course_code = models.CharField(max_length=300, default=None)
    course_name = models.CharField(max_length=300)
    duration = models.CharField(max_length=300, choices=DURATION_CHOICES, default=None)
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
    image = models.ImageField(upload_to='city_banners/', blank=True, null=True)
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
    location = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    language = models.CharField(max_length=1000, blank=True, null=True)
    certificate = models.CharField(max_length=1000, blank=True, null=True)
    fees = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.course} ({self.start_date} - {self.end_date})"

    class Meta:
        unique_together = ('course', 'city')

class Registration(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    job_title = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_country = CountryField()
    company_city = models.CharField(max_length=255)
    company_address = models.TextField()
    declaration = models.BooleanField()

    def __str__(self):
        return f"{self.name} - {self.course_offering}"