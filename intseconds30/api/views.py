from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpRequest
from django.urls import reverse

from .models import Card, Session


# Create your views here.
def index(request):
    return JsonResponse({"test": True})


def card_by_id(request, card_nr: int):
    try:
        card = Card.objects.get(number=card_nr)
        return JsonResponse({'card': card_nr, 'words': card.words_list})
    except ObjectDoesNotExist:
        print('Does not exist')
        return JsonResponse({"error": f"Card {card_nr} does not exist!"})


def get_token(request):
    session = Session()
    session.save()
    return JsonResponse({'token': session.id,
                         'secret': session.secret,
                         'get_card': f"{reverse('get-card')}?token={session.id}&secret={session.secret}"
                         })


def get_card(request: HttpRequest):
    token = request.GET.get('token')
    secret = request.GET.get('secret')

    # XOR on token and secret
    if token and not secret or not token and secret:
        return JsonResponse({'error': 'No token or secret'})
    elif token and secret:
        try:
            session = Session.objects.get(id=int(token), secret=secret)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Token expired or invalid"})

        if Card.objects.count() is session.used_cards.count():
            return JsonResponse({"error": "All cards have been used"})

        while True:
            card = Card.random()
            if card not in session.used_cards.all():
                session.used_cards.add(card)
                return JsonResponse(card.json())

    return JsonResponse(Card.random().json())
