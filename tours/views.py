from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views import View
from tours import data
from random import randint


class MainView(View):
    def get(self, request, *args, **kwargs):
        tours = {}
        while len(tours) < 6:
            tours_len = randint(1, len(data.tours))
            tours[tours_len] = data.tours[tours_len]

        title = data.title
        subtitle = data.subtitle
        description = data.description
        departures = data.departures

        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'departures': departures,
            'tours': tours,
        }
        return render(request, 'index.html', context)


class DepartureView(View):
    def get(self, request, *args, **kwargs):
        departure_code = kwargs['departure']
        title = data.title
        departures = data.departures
        tours = {id_: tour for id_, tour in data.tours.items() if tour['departure'] == departure_code}
        tours_num = len(tours)
        tours_min_price = min(tours.values(), key=lambda x: x['price'])['price']
        tours_max_price = max(tours.values(), key=lambda x: x['price'])['price']
        tours_min_price = str(tours_min_price)[:-3] + ' ' + str(tours_min_price)[-3:]
        tours_max_price = str(tours_max_price)[:-3] + ' ' + str(tours_max_price)[-3:]
        tours_min_nights = min(tours.values(), key=lambda x: x['nights'])['nights']
        tours_max_nights = max(tours.values(), key=lambda x: x['nights'])['nights']
        departure = departures[departure_code].split()[-1]

        context = {
            'departure_code': departure_code,
            'title': title,
            'departures': departures,
            'tours': tours,
            'tours_num': tours_num,
            'tours_min_price': tours_min_price,
            'tours_max_price': tours_max_price,
            'tours_min_nights': tours_min_nights,
            'tours_max_nights': tours_max_nights,
            'departure': departure
        }

        return render(request, 'departure.html', context)


class TourView(View):
    def get(self, request, *args, **kwargs):
        id_ = kwargs['id']
        title = data.title
        departures = data.departures
        departure_code = data.tours[id_]['departure']
        tour_title = data.tours[id_]['title']
        tour_description = data.tours[id_]['description']
        tour_departure = departures[departure_code].split()[1]
        tour_picture = data.tours[id_]['picture']
        tour_price = str(data.tours[id_]['price'])[:-3] + ' ' + str(data.tours[id_]['price'])[-3:]
        tour_stars = int(data.tours[id_]['stars']) * '★'
        tour_country = data.tours[id_]['country']
        tour_nights = data.tours[id_]['nights']
        tour_date = data.tours[id_]['date']

        context = {
            'title': title,
            'departures': departures,
            'departure_code': departure_code,
            'tour_title': tour_title,
            'tour_description': tour_description,
            'tour_departure': tour_departure,
            'tour_picture': tour_picture,
            'tour_price': tour_price,
            'tour_stars': tour_stars,
            'tour_country': tour_country,
            'tour_nights': tour_nights,
            'tour_date': tour_date,
        }
        return render(request, 'tour.html', context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините!')
