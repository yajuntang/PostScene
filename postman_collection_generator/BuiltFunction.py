from postman_collection_generator.models import Models


class BuiltFunction:

    @staticmethod
    def parse_built_function(value: str):
        if not isinstance(value, str): return value
        if not value.startswith('$'): return value
        value = value.strip()
        index = BuiltFunction.check_last_parentheses(value)
        if index == -1: value = value + '()'
        if index == -1: index = value.index(')')
        function_call = value[:index + 1]
        field = value[index + 1:]
        function_name = function_call[1:value.index('(')]
        params = function_call[function_call.index('(') + 1:-1].split(',')
        new_params = []
        for param in params:
            new_params.append(BuiltFunction.parse_built_function(param))

        if function_name == 'find':
            return Models.check_find.format(new_params[0], new_params[1], field)
        elif function_name == 'find_last':
            return Models.check_find_last.format(new_params[0], new_params[1], field)
        elif function_name == 'last':
            return '{0}[{0}.length - 1]{1}'.format(new_params[0], field)
        elif function_name == 'filter':
            if field == '': field = 'it'
            elif field.startswith('.'): field = 'it'+field
            return Models.check_filter.format(new_params[0],new_params[1], field)
        elif function_name == 'uuid32':
            return 'CryptoJS.MD5(new Date().getTime().toString()).toString()'
        elif function_name == 'timeS':
            return 'new Date({0}).getTime()'.format(new_params[0])
        elif function_name == 'times':
            return 'parseInt(new Date({0}).getTime()/1000)'.format(new_params[0])
        elif function_name == 'md5':
            return 'CryptoJS.MD5({0}).toString()'.format(new_params[0])
        elif function_name == 'weekStart':
            return Models.get_week_start
        elif function_name == 'weekEnd':
            return Models.get_week_end
        elif function_name == 'lastWeekStart':
            return Models.get_last_week_start
        elif function_name == 'lastWeekEnd':
            return Models.get_last_week_end
        elif function_name == 'monthStart':
            return Models.get_month_start
        elif function_name == 'monthEnd':
            return Models.get_month_end
        elif function_name == 'lastMonthStart':
            return Models.get_last_month_start
        elif function_name == 'lastMonthEnd':
            return Models.get_last_month_end
        elif function_name == 'last7DaysStart':
            return Models.get_before_date.format(-7)
        elif function_name == 'last30DaysStart':
            return Models.get_before_date.format(-30)
        elif function_name == 'dateFormat':
            return Models.date_format.format(new_params[0], new_params[1])
        else:
            return value

    @staticmethod
    def check_last_parentheses(value):
        stack = []
        index = 0
        for char in value:
            if char == '(':
                stack.append(index)
            elif char == ')':
                if len(stack) == 1:
                    return index
                else:
                    stack.pop()
            index = index + 1
        return -1
