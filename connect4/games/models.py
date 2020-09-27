from django.conf import settings
from django.db import models

# Create your models here.
from connect4.base.models import TimeStampedUUIDModel
from django.core.validators import MaxValueValidator, MinValueValidator

RED = "red"
YELLOW = "yellow"

COIN_CHOICES = (
    (RED, "Red"),
    (YELLOW, "Yellow"),
)


class Game(TimeStampedUUIDModel):
    INITIALIZED = "initialized"
    RUNNING = 'running'
    FINISHED = "finished"

    STATUS_CHOICES = (
        (RUNNING, "Running"),
        (FINISHED, "Finished"),
        (INITIALIZED, "Initialized"),
    )

    status = models.CharField(max_length=11, db_index=True, default=INITIALIZED, choices=STATUS_CHOICES)
    winner = models.CharField(max_length=6, db_index=True, blank=True, choices=COIN_CHOICES)

    def __str__(self):
        return self.id


class Move(TimeStampedUUIDModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    row = models.IntegerField(validators=[MaxValueValidator(settings.ROW_MAX_VALUE), MinValueValidator(0)], default=0, db_index=True)
    column = models.IntegerField(validators=[MaxValueValidator(settings.COLUMN_MAX_VALUE), MinValueValidator(0)], db_index=True)
    coin = models.CharField(max_length=6, db_index=True, choices=COIN_CHOICES)

    class Meta:
        unique_together = ("game", "row", "column")
        ordering = ("-created_at",)
