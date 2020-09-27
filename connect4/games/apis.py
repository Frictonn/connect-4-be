from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from connect4.games.models import Game
from connect4.games.serializers import MoveRetreieveSerializer, GameSerializer
from connect4.games.services import get_all_moves


class GameViewSet(viewsets.GenericViewSet):
    queryset = Game.objects.all()
    permission_classes = [AllowAny]
    serializer_classes = {
        "create": GameSerializer,
        "moves": MoveRetreieveSerializer
    }
    move_create_serializer = MoveRetreieveSerializer

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def __handle_new_move_addition(self, request, game_obj):
        context = self.get_serializer_context()
        context.update({"game_id": game_obj.id})
        serializer = self.move_create_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        move_obj = serializer.save(game=game_obj)
        response_serializer = self.get_serializer(move_obj)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def __handle_move_listing(self, request, game_obj):
        moves = get_all_moves(game_obj)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(moves, context=self.get_serializer_context(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        game_obj = Game.objects.create()
        serializer = self.get_serializer(game_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET", "POST"], detail=True)
    def moves(self, request, *args, **kwargs):
        game_obj = self.get_object()
        if request.method == "GET":
            return self.__handle_move_listing(request, game_obj)
        return self.__handle_new_move_addition(request, game_obj)
