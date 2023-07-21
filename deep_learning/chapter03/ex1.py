import numpy as np
#실습1 파이썬 코딩으로 구하느 최소 제곱
x = np.array([2,4,6,8])
y = np.array([81,93,91,97])
mx = np.mean(x)
my = np.mean(y)
print('x의 평균값 : ',mx)
print('y의 평균값 : ',my)
divisor = sum([(i-mx)**2 for i in x])
def top(x,mx,y,my):
    d = 0
    for i in range(len(x)):
        d += (x[i]-mx)*(y[i]-my)
    return d
dividend = top(x,mx,y,my)
print('')
print('분모', divisor)
print('분자', dividend)
a = dividend/divisor
b = my -(mx*a)
print('')
print('기울기 a = ',a)
print('y 절편 b = ',b)