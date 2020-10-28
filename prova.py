

def funzione1(a):
    return a+1

def funzione2(b):
    return 2*b

def main():

    fl = [funzione1, funzione2]

    for f in fl:
        print(f(5))
    

if __name__ == "__main__":
    main()    