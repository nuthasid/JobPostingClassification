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


def balance_training_set(dataset: list, target, field):
    """From a list of dataset which contain more than one class -
    as indicated by field, return a list of dataset which contain
    equal number of target classes - target and the rest."""
    import random
    pos_class = []
    neg_class = []
    for item in dataset:
        if item[field] == target:
            pos_class.append(item)
        else:
            neg_class.append(item)
    if len(pos_class) > len(neg_class):
        ret_dat = neg_class + random.sample(pos_class, len(neg_class))
        random.shuffle(ret_dat)
        return ret_dat
    elif len(pos_class) < len(neg_class):
        ret_dat = pos_class + random.sample(neg_class, len(pos_class))
        random.shuffle(ret_dat)
        return ret_dat
    else:
        return dataset


def classify_en_th(document):
    """Classify English documents from Thai documents and vise-versa
    based on character count."""
    th_count = 0
    en_count = 0
    for char in document:
        if ord(char) in range(3585, 3678):
            th_count += 1
        elif ord(char) in range(65, 122):
            en_count += 1
    if en_count >= th_count:
        return 'en'
    else:
        return 'th'
