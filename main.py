import poker.calc
import time


def main():
    # 時間計測
    start = time.time()

    res = poker.calc.getMaxExpectation('J', 's7', 'h4', 's5', 'sk',)
    print(res)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    main()
