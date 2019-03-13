from time import sleep, time
users = [2,4]
def method1(car = 0, started = False):
    for user in users:
        print(user)
        sleep(1)
    print(car)
    print(started)


method1(car = 1)
