from lark import Lark
import os

mini_lisp_grammar = ""
with open("grammar.lark", 'r', encoding='utf-8') as f:
    mini_lisp_grammar = f.read()

# print(mini_lisp_grammar)

mini_lisp_parser = Lark(mini_lisp_grammar, start='program')

def type_check(parameter, type_):
    if type_ == "int":
        # print("int: ", isinstance(parameter, int))
        return type(parameter) == int
    elif type_ == "bool":
        # print("bool: ", isinstance(parameter, bool))
        return type(parameter) == bool
    # elif type == "fun":
    #     return isinstance(parameter, Lark)
    return False

global_env = {}

def eval_ast(tree, param=None, local_env=None, fun_ids=False, def_fun=False, def_nested_fun=False):
    # print("cur tree: " + tree.data)
    # if local_env:
    #     print(tree.data + " local_env: " + str(local_env))
    if tree.data == 'program':
        # print(tree.children)
        for child in tree.children:
            eval_ast(child)
    elif tree.data == 'def_stmt':
        # print(tree.children)
        var = eval_ast(tree.children[0])
        val = eval_ast(tree.children[1], def_fun=True)

        if def_nested_fun:
            return {var: val}

        global_env[var] = val
        # print("def_stmt var: " + var)
        # print("def_stmt val: " + str(val))
    elif tree.data == 'variable':
        # print(tree.children)
        return eval_ast(tree.children[0], local_env=local_env)
    elif tree.data == 'print_num':
        # print(tree.children)
        val = eval_ast(tree.children[0])
        print(str(val))
    elif tree.data == 'print_bool':
        # print(tree.children)
        val = eval_ast(tree.children[0])
        if val:
            print("#t")
        else:
            print("#f")
    elif tree.data == 'plus':
        # print(tree.children)
        # result = sum([eval_ast(child, local_env=local_env) for child in tree.children])
        result = 0
        for child in tree.children:
            num = eval_ast(child, local_env=local_env)
            if not type_check(num, "int"):
                raise Exception("Type Error")
            result += num
        # print("plus: " + str(result))
        return result
    elif tree.data == 'minus':
        # print(tree.children)
        # result = eval_ast(tree.children[0], local_env=local_env) - eval_ast(tree.children[1], local_env=local_env)
        num1 = eval_ast(tree.children[0], local_env=local_env)
        num2 = eval_ast(tree.children[1], local_env=local_env)
        if not type_check(num1, "int") or not type_check(num2, "int"):
            raise Exception("Type Error")
        result = num1 - num2
        # print("minus: " + str(result))
        return result
    elif tree.data == 'multiply':
        # print(tree.children)
        result = 1
        for child in tree.children:
            num = eval_ast(child, local_env=local_env)
            if not type_check(num, "int"):
                raise Exception("Type Error")
            result *= num
        # print("multiply: " + str(result))
        return result
    elif tree.data == 'divide':
        # print(tree.children)
        # result = int(eval_ast(tree.children[0], local_env=local_env) / eval_ast(tree.children[1], local_env=local_env))
        num1 = eval_ast(tree.children[0], local_env=local_env)
        num2 = eval_ast(tree.children[1], local_env=local_env)
        if not type_check(num1, "int") or not type_check(num2, "int"):
            raise Exception("Type Error")
        result = int(num1 / num2)
        # print("divide: " + str(result))
        return result
    elif tree.data == 'modulus':
        # print(tree.children)
        # result = eval_ast(tree.children[0], local_env=local_env) % eval_ast(tree.children[1], local_env=local_env)
        num1 = eval_ast(tree.children[0], local_env=local_env)
        num2 = eval_ast(tree.children[1], local_env=local_env)
        if not type_check(num1, "int") or not type_check(num2, "int"):
            raise Exception("Type Error")
        result = num1 % num2
        # print("modulus: " + str(result))
        return result
    elif tree.data == 'greater':
        # print(tree.children)
        # result = eval_ast(tree.children[0], local_env=local_env) > eval_ast(tree.children[1], local_env=local_env)
        num1 = eval_ast(tree.children[0], local_env=local_env)
        num2 = eval_ast(tree.children[1], local_env=local_env)
        if not type_check(num1, "int") or not type_check(num2, "int"):
            raise Exception("Type Error")
        result = num1 > num2
        # print("greater: " + str(result))
        return result
    elif tree.data == 'smaller':
        # print(tree.children)
        # result = eval_ast(tree.children[0], local_env=local_env) < eval_ast(tree.children[1], local_env=local_env)
        num1 = eval_ast(tree.children[0], local_env=local_env)
        num2 = eval_ast(tree.children[1], local_env=local_env)
        if not type_check(num1, "int") or not type_check(num2, "int"):
            raise Exception("Type Error")
        result = num1 < num2
        # print("smaller: " + str(result))
        return result
    elif tree.data == 'equal':
        # print(tree.children)
        first_num = eval_ast(tree.children[0], local_env=local_env)
        if not type_check(first_num, "int"):
            raise Exception("Type Error")
        for i in range(1, len(tree.children)):
            cur_num = eval_ast(tree.children[i], local_env=local_env)
            if not type_check(cur_num, "int"):
                raise Exception("Type Error")
            if first_num != cur_num:
                # print("equal: False")
                return False
        # print("equal: True")
        return True
    elif tree.data == 'and_op':
        # print(tree.children)
        # result = all([eval_ast(child, local_env=local_env) for child in tree.children])
        result = True
        for child in tree.children:
            bool = eval_ast(child, local_env=local_env)
            if not type_check(bool, "bool"):
                raise Exception("Type Error")
            if not bool:
                result = False
                break
        # print("and: " + str(result))
        return result
    elif tree.data == 'or_op':
        # print(tree.children)
        # result = any([eval_ast(child, local_env=local_env) for child in tree.children])
        result = False
        for child in tree.children:
            bool = eval_ast(child, local_env=local_env)
            if not type_check(bool, "bool"):
                raise Exception("Type Error")
            if bool:
                result = True
                break
        # print("or: " + str(result))
        return result
    elif tree.data == 'not_op':
        # print(tree.children)
        # result = not eval_ast(tree.children[0], local_env=local_env)
        bool = eval_ast(tree.children[0], local_env=local_env)
        if not type_check(bool, "bool"):
            raise Exception("Type Error")
        result = not bool
        # print("not: " + str(result))
        return result
    elif tree.data == 'if_exp':
        # print(tree.children)
        test = eval_ast(tree.children[0], local_env=local_env)
        if not type_check(test, "bool"):
            raise Exception("Type Error")
        # print("test result: " + str(test))
        if test:
            then = eval_ast(tree.children[1], local_env=local_env)
            # print("then: " + str(then))
            return then
        else:
            els = eval_ast(tree.children[2], local_env=local_env)
            # print("else: " + str(els))
            return els
    elif tree.data == 'test_exp':
        # print(tree.children)
        result = eval_ast(tree.children[0], local_env=local_env)
        # print("test: " + str(result))
        return result
    elif tree.data == 'than_exp':
        # print(tree.children)
        result = eval_ast(tree.children[0], local_env=local_env)
        # print("than: " + str(result))
        return result
    elif tree.data == 'else_exp':
        # print(tree.children)
        result = eval_ast(tree.children[0], local_env=local_env)
        # print("else: " + str(result))
        return result
    elif tree.data == 'fun_call':
        # print(tree.children)
        param = []
        for i in range(1, len(tree.children)):
            # print(tree.children[i])
            param.append(eval_ast(tree.children[i], local_env=local_env))
        # print("parm:", param)
        # print(param)
        result = eval_ast(tree.children[0], param=param, local_env=local_env)
        # print("fun_call: " + str(result))
        return result
    elif tree.data == 'param':
        # print(tree.children)
        return eval_ast(tree.children[0], local_env=local_env, def_fun=True)
    elif tree.data == 'fun_exp':
        # print(tree.children)
        if def_fun:
            return tree
        
        local_vars = eval_ast(tree.children[0])
        # print("local_vars: " + str(local_vars))
        if local_vars: # 帶有區域變數的函式
            local_env = dict(zip(local_vars, param))
            # print("local_env: " + str(local_env))
            result = eval_ast(tree.children[1], local_env=local_env)
            # print("fun_exp: " + str(result))
            return result
        else: # 無區域變數的函式
            result = eval_ast(tree.children[1])
            # print("fun_exp: " + str(result))
            return result
    elif tree.data == 'fun_ids':
        # print(tree.children)
        local_vars = []
        for child in tree.children:
            local_vars.append(eval_ast(child, fun_ids=True))
        # print("fun_ids: " + str(local_vars))
        return local_vars
    elif tree.data == 'fun_body':
        # result = eval_ast(tree.children[0], local_env=local_env)
        # print(tree.children)
        result = None
        for child in tree.children:
            if child.data == 'def_stmt':
                local_fun = eval_ast(child, local_env=local_env, def_nested_fun=True)
                # print("local_fun:", local_fun)
                local_env.update(local_fun)
            else:
                # print("else child:", child)
                # print("local_env:", local_env)
                result = eval_ast(child, local_env=local_env)
        # print("fun_body: " + str(result))
        return result
    elif tree.data == 'fun_name':
        fun_tree = eval_ast(tree.children[0], local_env=local_env)
        # print("fun_tree:", fun_tree)
        # print("param:", param)
        result = eval_ast(fun_tree, param=param)
        # print("fun_name: " + str(result))
        return result
    elif tree.data == 'id':
        # print(tree.children)
        # print("id: " + tree.children[0])
        # print("id check local_env:", local_env)
        if local_env and tree.children[0] in local_env:
            return local_env[tree.children[0]]
        if not fun_ids and tree.children[0] in global_env:
            return global_env[tree.children[0]]
        return tree.children[0]
    elif tree.data == 'number':
        # print(tree.children)
        # print("number: " + tree.children[0])
        return int(tree.children[0])
    elif tree.data == 'bool_val':
        # print(tree.children)
        if tree.children[0] == "#t":
            return True
        return False
    
folder_path = './public_test_data'

for root, dirs, files in os.walk(folder_path):
    for file in files:
        # print(os.path.join(root, file))
        code = ""
        # file_path = "./public_test_data/b2_2.lsp"
        file_path = os.path.join(root, file)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
        except FileNotFoundError:
            print(f"檔案 {file_path} 不存在。")
        except Exception as e:
            print(f"讀取檔案時發生錯誤: {e}")

        # code = """
        # """

        print(file_path)
        # print("檔案內容:")
        # print(code)
        try:
            global_env = {} # 清空環境
            tree = mini_lisp_parser.parse(code)
            # print(tree.pretty())
            eval_ast(tree)
        except Exception as e:
            if str(e) == "Type Error":
                print("Type Error")
            else:
                # print("syntax error: ", e)
                print("syntax error")
        print()