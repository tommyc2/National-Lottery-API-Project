def hello(**args):
    for val in args.values():
        print(val)

hello(val1="hello", val2="Tommy")