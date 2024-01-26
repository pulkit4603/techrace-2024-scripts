import random
# 1-1 = 2-1 = 3-1
# 1-13 = 2-13 = 3-13
def random_route():
    route = {}
    for i in range(1, 14):
        route_no = random.choice([1, 2])
        route[f'c{i}'] = (f'{route_no}-{i}')
    return route
