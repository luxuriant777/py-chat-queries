from db.models import Message, User, Chat

from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(User.objects.filter(
        message__sent__year=2015
    ).values_list("first_name", "last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(message__sent__year__gt=2020))


def get_messages_contain_authors_first_name() -> list[Message]:
    return list(Message.objects.filter(text__icontains=F("user__first_name")))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__startswith="a")
        | Q(message__text__startswith="m")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=True)
        | Q(user__username__istartswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).aggregate(Count("id"))["id__count"]


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("message__user_id")).order_by("-num_messages"))[:3]


def get_last_5_messages_dicts() -> list[dict]:
    result = []
    for message in Message.objects.order_by(
            "-sent")[:5].select_related("user"):
        result.append({"from": message.user.username, "text": message.text})
    return result


def get_chat_dicts() -> list[dict]:
    result = []
    for chat in Chat.objects.all().prefetch_related("users"):
        users = [user.username for user in chat.users.all()]
        result.append({"id": chat.id, "title": chat.title, "users": users})
    return result
