class BuiltFunction:
    @staticmethod
    def smart_split(s: str, delimiter: str = ','):
        """支持括号感知的参数分割"""
        parts = []
        bracket_level = 0
        current_part = []
        for char in s:
            if char == '(':
                bracket_level += 1
            elif char == ')':
                bracket_level -= 1

            if char == delimiter and bracket_level == 0:
                parts.append("".join(current_part).strip())
                current_part = []
            else:
                current_part.append(char)
        parts.append("".join(current_part).strip())
        return parts

    @staticmethod
    def parse_built_function(value: str):
        """解析内置函数调用"""
        if not isinstance(value, str) or not value.startswith('$'):
            return value

        value = value.strip()
        last_paren_idx = BuiltFunction.get_closing_paren_idx(value)

        if last_paren_idx == -1:
            value += '()'
            last_paren_idx = value.rfind(')')

        call_part = value[:last_paren_idx + 1]
        field_part = value[last_paren_idx + 1:]

        open_paren_idx = call_part.find('(')
        func_name = call_part[1:open_paren_idx]
        raw_params = call_part[open_paren_idx + 1:-1]

        params = [BuiltFunction.parse_built_function(p) for p in BuiltFunction.smart_split(raw_params) if p]

        from post_scene.models import Models
        # 使用映射字典提高可读性
        mapping = {
            'find': lambda p, f: Models.check_find.format(p[0], p[1], f),
            'uuid32': lambda p, f: 'CryptoJS.MD5(new Date().getTime().toString()).toString()',
            'md5': lambda p, f: f'CryptoJS.MD5({p[0]}).toString()',
            'dateFormat': lambda p, f: Models.date_format.format(p[0], p[1]),
            'weekStart': lambda p, f: Models.get_week_start,
            'monthStart': lambda p, f: Models.get_month_start,
        }

        if func_name in mapping:
            return mapping[func_name](params, field_part)
        return value

    @staticmethod
    def get_closing_paren_idx(value):
        """精确定位外层括号索引"""
        stack = []
        for i, char in enumerate(value):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if len(stack) == 1: return i
                if stack: stack.pop()
        return -1