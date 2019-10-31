def user_select_option(message, options):
    option_list = list(options)
    print(message)
    for i, val in enumerate(option_list):
        print(i, ': ' + val["name"])
    index = int(input("Enter choice (default 0): ") or 0)
    return option_list[index]