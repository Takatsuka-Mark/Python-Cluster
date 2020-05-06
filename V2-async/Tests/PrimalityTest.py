from V2.Problem.Primality import PrimalityTest

if __name__ == '__main__':
    prim = PrimalityTest()
    prim.run(2, 100)
    print(prim.res)
    print(len(prim.res))
