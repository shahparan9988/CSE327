from django.db import models
from django.core.exceptions import ObjectDoesNotExist
# Using PositiveIntegerField we can easily specify the order of objects

# custom order Field -> inherits PositiveIntegerField
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields #indicates the field that the order
                                      #has to be calculated with respect to
        super(OrderField, self).__init__(*args, **kwargs)

    # executes before saving the field in database
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            #no current value
            try:
                qs = self.models.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field)\
                    for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField,
                         self).pre_save(model_instance, add)
