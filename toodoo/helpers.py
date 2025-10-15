from datetime import date


def get_due_status(task):
    delta = (task.due_date - date.today()).days

    if delta < 0:
        return f'{-delta} days'
    elif delta == 1:
        return f'{1} day'
    elif delta > 1:
        return f'{delta} days'
    else: 
        return f'Due Today'