from collections import defaultdict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from connect4.games.models import Move, Game
from connect4.games.services import is_valid_move


class MoveCreateSerializer(serializers.ModelSerializer):
    row = serializers.IntegerField(required=False, allow_null=False)

    def validate(self, attrs):
        validation_errors = defaultdict(list)
        column = attrs.get("column")
        coin = attrs.get("coin")
        game_id = self.context.get("game_id", None)
        is_valid, row, description = is_valid_move(game_id, column, coin)

        if not is_valid:
            validation_errors["coin"].append(description)

        # Raise all errors at once
        if validation_errors:
            raise ValidationError(validation_errors)
        self.context.update({"row": row})
        return super(MoveCreateSerializer, self).validate(attrs)

    class Meta:
        model = Move
        fields = ["id", "column", "coin", "created_at"]

    def create(self, validated_data):
        row = self.context.get("row", 0)
        validated_data['row'] = row
        return super().create(validated_data)


class MoveRetreieveSerializer(MoveCreateSerializer):
    game_status = serializers.SerializerMethodField()
    game_winner = serializers.SerializerMethodField()

    class Meta(MoveCreateSerializer.Meta):
        fields = MoveCreateSerializer.Meta.fields + ["row", "game_status", "game_winner"]

    def get_game_status(self, obj):
        return obj.game.status

    def get_game_winner(self, obj):
        return obj.game.winner


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ["id", "status", "winner", "moves"]
