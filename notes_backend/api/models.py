from django.db import models
from django.contrib.auth import get_user_model


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Note(TimeStampedModel):
    """
    Note model linked to a user. Each note is private to its owner.
    """
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notes",
        db_index=True,
        help_text="The user that owns this note."
    )
    title = models.CharField(max_length=255, help_text="Title of the note.")
    content = models.TextField(blank=True, help_text="Body/content of the note.")
    is_archived = models.BooleanField(default=False, help_text="Whether the note is archived.")

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["owner", "is_archived"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} (owner={self.owner_id})"
