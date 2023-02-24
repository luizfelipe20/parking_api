import uuid
from django.db import models
from datetime import datetime, timezone, timedelta


class Historic(models.Model):
    reserve = models.CharField("reserva", max_length=6)
    plate = models.CharField("placa", max_length=8)
    entry_time = models.DateTimeField(
        "horário de entrada", auto_now_add=True, auto_now=False
    )
    departure_time = models.DateTimeField("horário de saída", null=True, blank=True)
    paid = models.BooleanField("pagamento", default=False)
    left = models.BooleanField("saida", default=False)

    class Meta:
        verbose_name = "historic"
        verbose_name_plural = "Historics"

    def save(self, *args, **kwargs):
        self.reserve = uuid.uuid4().hex[0:6]

        if self.left:
            self.departure_time = datetime.now(timezone.utc)

        super(Historic, self).save(*args, **kwargs)

    @property
    def period(self):
        _period = ""
        if self.departure_time:
            # import ipdb; ipdb.set_trace()
            _period = (self.departure_time - self.entry_time).total_seconds()
            return str(timedelta(seconds=_period))
        return _period