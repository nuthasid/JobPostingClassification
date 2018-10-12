def wrapper(func, arg_names, **kwargs):
    """
    Wrapper function, which can be used as a decorator, to be used for reducing number of arguments.


    :param func: The function into which to be wrapped.
    :param arg_names: List of the name(s) of the argument(s) to be passed onto the wrapped function.
                        Argument(s), which can be a single parameter or a list of parameters,
                        to be passed into wrapped function must be in the same order as arg_names.
    :param kwargs: A dictionary {arg_name:value} to be fixed onto the wrapped function.
    :return: Wrapped function wherein only arguments in [arg_name] are to be passed.
    """

    def wrapped_function(args):
        if not type(args) in (list, tuple):
            args = (args,)
        else:
            args = tuple(args)
        args = zip(arg_names, args)
        for arg in args:
            kwargs[arg[0]] = arg[1]
        return func(**kwargs)
    if not type(arg_names) in (list, tuple):
        arg_names = (arg_names,)
    return wrapped_function
