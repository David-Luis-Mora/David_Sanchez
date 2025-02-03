from shared.serializers import BaseSerializer


class TokensSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': {
                'id': instance.user.id,
                'username': instance.user.username,
                'email': instance.user.email,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'email': instance.user.email
            },
            'key': instance.key,
            'created_at': instance.created_at,
        }
