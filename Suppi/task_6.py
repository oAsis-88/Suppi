import pandas as pd

from main import assigning_category
from task_5 import function_5

dataFrame = pd.read_json('resources/trial_task.json')


def function_6(data):
    tmp_data = function_5(data)
    result = assigning_category(tmp_data)
    return result


print(function_6(dataFrame))
