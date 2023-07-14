def test_singer(var_singer):
    print(id(var_singer))
    var_singer = 0
    print(id(var_singer))
    print(var_singer)


def test_list(var_list):
    var_list[0] = 999
    print(var_list)

v = 10
t_t = test_singer(v)
print(v)

v_l = [0, 2, 4, 6]
t_l = test_list(v_l)
print(v_l)



