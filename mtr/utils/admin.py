class OriginalQuerysetMixin(object):

    def get_queryset(self, request):
        """Returns a QuerySet of all model instances without default
        manager 'objects' that can be edited by the
        admin site. This is used by changelist_view."""

        qs = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
