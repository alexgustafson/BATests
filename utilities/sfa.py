def sfa(radii):

    max = None
    radius_difference_threshold = 0.1

    for angle in range(0, 181):

        SFAa = 0

        for i in range(1, 180):

            r1 = radii[angle + i]['distance']
            r2 = radii[angle - i]['distance']
            difference = abs(r1 - r2)
            if r1 < r2:
                difference_in_precentage = difference / r1
            else:
                difference_in_precentage = difference / r2

            if difference_in_precentage <= radius_difference_threshold:
                SFAa += 1

        radii[angle]['SFAa'] = SFAa

        if not max or radii[angle]['SFAa'] > max['SFAa']:
            max = radii[angle]

    perpendicular = 0

    if max['angle'] > 90:
        perpendicular = max['angle'] - 90
    else:
        perpendicular = max['angle'] + 90

    return max, radii[perpendicular]