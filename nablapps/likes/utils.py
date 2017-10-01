from django.contrib.contenttypes.models import ContentType


class LikeException(Exception):
    def __init__(self, message):
        self.message = message


def get_object(contenttype_id, object_id):
    try:
        content_type = ContentType.objects.get(id=contenttype_id)
        object = content_type.get_object_for_this_type(id=object_id)
    except ContentType.DoesNotExist:
        raise LikeException(
                "ContentType with id {} does not exist".format(contenttype_id))
    except content_type.model_class().DoesNotExist:
        raise LikeException(
                "{} with id {} does not exist".format(content_type.model, object_id))
    return object
