from lexer import run


while True:
    try:
        inp = input("basic > ")
        if inp == "exit()":
            break
        tokens, error = run("<stdin>", inp)
        if error:
            print(error.to_string())
        else:
            print(tokens)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        continue
    