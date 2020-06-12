from django.db import models

class CenterManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, admin):
        return self.filter(admin=admin)


class JoinRequestManager(models.Manager):
    use_for_related_fields = True

    def created_by(self, professor):
        return self.filter(professor=professor)
