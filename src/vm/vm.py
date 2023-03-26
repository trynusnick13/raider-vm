from vm.utils import extract_all_commands

LOCAL_VARIABLES_ARRAY: list[int] = [0] * 16
STACK: list[int] = []


def run_bytecode(file_name: str, is_debug_mode: bool = False):
    global LOCAL_VARIABLES_ARRAY, STACK

    all_ops: list[str] = extract_all_commands(file_name=file_name)

    counter = 0
    while counter < len(all_ops):
        op = all_ops[counter]
        if is_debug_mode:
            print("-" * 50)
            print(f"Current Stack: {STACK}")
            print(f"Current Op is '{op}'")

        match op.split(): # Params validation needs to be provided
            case ["iconst", param]:
                STACK.append(int(param))
            case ["istore", param]:
                LOCAL_VARIABLES_ARRAY[int(param)] = STACK.pop()
            case ["increment", param]:
                LOCAL_VARIABLES_ARRAY[int(param)] = LOCAL_VARIABLES_ARRAY[int(param)] + 1
            case ["iload", param]:
                STACK.append(LOCAL_VARIABLES_ARRAY[int(param)])
            case ["print", param]:
                print(LOCAL_VARIABLES_ARRAY[int(param)])
            case ["iadd", param]:
                total_sum = 0
                for _ in range(int(param)):
                    total_sum += STACK.pop()
                STACK.append(total_sum)
            case ["imult", param]:
                total_mult = 0
                for _ in range(int(param)):
                    total_mult *= STACK.pop()
            case ["lt_cmp"]:
                right_operand = STACK.pop()
                left_operand = STACK.pop()
                cmp_result: int = int(left_operand < right_operand)
                STACK.append(cmp_result)
            case ["fw_jump", param]:
                cmp_result: int = STACK.pop()
                if not cmp_result:
                    for _ in range(int(param)):
                        counter += 1
            case ["bck_jump", param]:
                for _ in range(int(param) + 1): # брудна гра
                    counter -= 1

        counter += 1

        if is_debug_mode:
            print(f"Current Stack: {STACK}")


if __name__ == "__main__":
    run_bytecode("script.raided")
