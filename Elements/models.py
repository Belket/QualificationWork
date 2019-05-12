from django.db import models
from HandBook.models import Company, Class, Group, SubGroup
from django.dispatch import receiver
from django.db.models.signals import post_save


class Element(models.Model):
    class Meta:
        verbose_name = "Element"
        verbose_name_plural = "Elements"
    name = models.CharField(max_length=100, blank=False)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    Subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    T0 = models.FloatField(blank=False)
    Txp = models.FloatField(blank=False)
    Tp = models.FloatField(blank=False)
    TB = models.FloatField(blank=False)
    Info = models.TextField(blank=True)
    date_of_adding = models.DateField(blank=False)
    confirm_link = models.CharField(max_length=100, default="None")

    def save(self, *args, **kwargs):
        T0 = self.T0
        lambda0 = 1 / T0
        lambda_xp = lambda0 * 10 ** (-2)
        self.Txp = 1 / (lambda_xp * 8760)
        self.Tp = (1 - 0.15 * 0.253) * T0
        super(Element, self).save(*args, **kwargs)


@receiver(post_save, sender=Element)
def calculate_means(sender, instance, **kwargs):
    subgroup = instance.Subgroup
    elements = Element.objects.filter(Subgroup=subgroup)
    amount_of_elements = len(elements)
    subgroup.minT0 = sum([element.T0 for element in elements]) / amount_of_elements
    subgroup.minTxp = sum([element.Txp for element in elements]) / amount_of_elements
    subgroup.minTp = sum([element.Tp for element in elements]) / amount_of_elements
    subgroup.minTB = sum([element.TB for element in elements]) / amount_of_elements
    subgroup.save()



