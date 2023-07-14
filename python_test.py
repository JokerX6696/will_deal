def test_singer(var_singer):
    print("变量进入函数初始地址为: " + str(id(var_singer)))
    var_singer = 0
    print("变量在函数内经过函数重新赋值后为: " + str(var_singer))
    print("变量在函数内经过函数重新赋值后地址为: " + str(id(var_singer)))

def test_list(var_list):
    var_list[0] = 999
    print("变量在函数内经过函数重新赋值后为: ",end='')
    print(var_list)

v = 10
print("变量在全局变量中初始地址为: " + str(id(v)))
t_t = test_singer(v)
print("变量在经过函数重新赋值后地址为: " + str(id(v)))

v_l = [0, 2, 4, 6]
print("变量初始列表为",end='')
print(v_l)
print("变量在全局变量中初始地址为: " + str(id(v_l)))
t_l = test_list(v_l)
print("变量在函数内经过函数重新赋值后外部变量为: ",end='')
print(v_l)
 


