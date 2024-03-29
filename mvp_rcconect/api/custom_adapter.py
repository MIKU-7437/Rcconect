from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from allauth.utils import build_absolute_uri


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "api_rcconnect:rest_verify_email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url)
        return ret
