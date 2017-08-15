from django.conf import settings
from django.core.signing import BadSignature, Signer
from django.utils.functional import SimpleLazyObject, empty

from .models import LikeList


class LikeListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        request.cookies_to_delete = []
        request._likelist_cache = None
        request.likelist = self.get_likelist(request)

        return request


    def process_response(self, request, response):
        # Delete any surplus cookies
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'likelist'):
            return response

        cookie_key = 'likelist'
        # Check if we need to set a cookie. If the cookies is already available
        # but is set in the cookies_to_delete list then we need to re-set it.
        has_likelist_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)

        if (request.likelist and not has_likelist_cookie):
            cookie = self.get_likelist_hash(request.likelist.id)
            response.set_cookie(
                cookie_key, cookie,
                max_age=getattr(settings, 'LIKELIST_COOKIE_LIFETIME', 365*24*60*60),
                httponly=True)
        return response

    def get_likelist(self, request):
        """
        Return the open likelist for this request
        """
        if request._likelist_cache is not None:
            return request._likelist_cache


        cookie_likelist = self.get_cookie_likelist(request)

        if cookie_likelist:

            likelist = cookie_likelist
        else:

            likelist = LikeList()
            likelist.save()

        request._likelist_cache = likelist

        return likelist

    def get_cookie_likelist(self, request):

        likelist = None
        if 'likelist' in request.COOKIES:
            likelist_hash = request.COOKIES['likelist']

            try:
                likelist_id = Signer().unsign(likelist_hash)
                likelist = LikeList.objects.get(pk=likelist_id)
            except (BadSignature, LikeList.DoesNotExist):
                request.cookies_to_delete.append('likelist')
        return likelist

    def get_likelist_hash(self, likelist_id):
        return Signer().sign(likelist_id)
