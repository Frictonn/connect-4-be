from rest_framework.routers import DefaultRouter

from connect4.games.apis import GameViewSet

default_router = DefaultRouter(trailing_slash=False)


default_router.register("games", GameViewSet, basename="games")


urlpatterns = default_router.urls
