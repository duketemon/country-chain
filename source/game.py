from collections import defaultdict


class Game:

    __countries_ids = defaultdict(list)
    __countries = dict()
    __lowered_countries = dict()

    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            words = f.read().split('\n')
            for id_, word in enumerate(words):
                self.__countries_ids[word[0].lower()].append(id_)
                self.__countries[id_] = word
                self.__lowered_countries[id_] = word.lower()

    def get_country(self, country_id: int) -> str:
        return self.__countries[country_id]

    def next_move(self, requested_country: str, used_counties: {int}):
        for countries_id in self.__countries_ids[requested_country[-1].lower()]:
            if countries_id not in used_counties:
                return countries_id, self.__countries[countries_id]
        return None, None

    def get_country_id(self, requested_country: str):
        requested_country = requested_country.lower()
        for country_id in self.__countries_ids[requested_country[0]]:
            if requested_country == self.__lowered_countries[country_id]:
                return country_id
        return None

    def have_candidates(self, requested_country: str, used_counties: {int}) -> bool:
        requested_country = requested_country.lower()
        for country_id in self.__countries_ids[requested_country[-1]]:
            if country_id not in used_counties:
                return True
        return False

