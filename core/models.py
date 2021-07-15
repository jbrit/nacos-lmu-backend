from core.validators import course_code_validator, year_2xxx_validator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model"""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self) -> str:
        return self.email


# App Logic models
class Semester(models.Model):
    """Model for a semester with a start year, end year and semester type (alpha|omega)"""
    
    class SemesterTypeChoices(models.Choices):
        ALPHA = "ALPHA"
        OMEGA = "OMEGA"

    start_year = models.PositiveBigIntegerField(validators=[year_2xxx_validator])
    end_year = models.PositiveBigIntegerField(validators=[year_2xxx_validator])
    type = models.CharField(choices=SemesterTypeChoices.choices, max_length=5, blank=False)

    def clean(self, *args, **kwargs):
        if self.end_year - self.start_year != 1:
            raise ValidationError({
                    'end_year': _('End year should come immediately after the start year'),
                })
    
    def __str__(self) -> str:
        return f"{self.start_year}/{self.end_year} {self.type} Semester"

class Course(models.Model):
    """Course Model with code field, in the format: MAT 111 (strictly)"""
    code = models.CharField(max_length=7, validators=[course_code_validator])

    def __str__(self) -> str:
        return f"{self.code}"

class PastQuestion(models.Model):
    """Model for a semester with a start year, end year and semester type (alpha|omega)"""
    
    def course_directory_path(instance, filename):
        return 'past_questions/{0}/{1}'.format(str(instance.course), filename)

    class PastQuestionTypeChoices(models.Choices):
        EXAM = "EXAM"
        CA = "CA"

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(choices=PastQuestionTypeChoices.choices, max_length=4, blank=False)
    file = models.FileField(upload_to=course_directory_path)

    def __str__(self) -> str:
        return f"{self.course} {self.type} {self.semester}"

    class Meta:
        unique_together = ("semester", "course", "type")
