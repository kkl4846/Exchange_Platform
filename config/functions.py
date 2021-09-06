from jamo import h2j, j2hcj


def order_domestic(universities):
    universities_dict = {}
    last_cho = 'ㄱ'
    universities_dict[last_cho] = []

    for university in universities:
        this_university = university.home_name
        university_cho = j2hcj(h2j(this_university[0]))[0]
        if last_cho != university_cho:     # 직전 초성과 다른 초성
            universities_dict[university_cho] = []
            universities_dict[university_cho].append(university)
            last_cho = university_cho
        else:                           # 같은 초성
            universities_dict[university_cho].append(university)

    g_cho = 'ㄱ'
    if len(universities_dict[g_cho]) == 0:
        del(universities_dict[g_cho])
    return universities_dict


def order_country(countries):
    countries_dict = {}
    last_alpha = 'ㄱ'
    countries_dict[last_alpha] = []

    for country in countries:
        this_country = country.country_name
        this_alpha = j2hcj(h2j(this_country[0]))[0]
        if last_alpha != this_alpha:
            countries_dict[this_alpha] = []
            countries_dict[this_alpha].append(country)
            last_alpha = this_alpha
        else:
            countries_dict[this_alpha].append(country)
    g_cho = 'ㄱ'
    if len(countries_dict[g_cho]) == 0:
        del(countries_dict[g_cho])
    return countries_dict


def order_foreign(univs):
    univ_dict = {}
    last_alpha = 'A'
    univ_dict[last_alpha] = []
    for univ in univs:
        u = univ.away_name
        this_alpha = u[0]
        if last_alpha != this_alpha:
            univ_dict[this_alpha] = []
            univ_dict[this_alpha].append(univ)
            last_alpha = this_alpha
        else:
            univ_dict[this_alpha].append(univ)
    if len(univ_dict['A']) == 0:
        del(univ_dict['A'])
    return univ_dict
