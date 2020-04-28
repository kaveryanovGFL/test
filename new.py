old_price = 29
new_prise = 31
if ((old_price - new_prise) >= 3 or (new_prise - old_price) >= 3):
    print('new = {}, old = {}, res = {}'.format(old_price, new_prise, old_price - new_prise))
    old_price = new_prise
