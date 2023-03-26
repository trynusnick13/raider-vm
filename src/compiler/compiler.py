from compiler.commands import assign_variable
from compiler.commands import increment_var
from compiler.commands import show_value
from compiler.commands import compare_values
from compiler.commands import run_cycle



LOCAL_VARIABLES_COUNTER = 0
OPS_STACK = []
VARIABLES_MAPPING = {}


def compile(file_name: str, is_debug_mode: bool = False) -> str:
    global LOCAL_VARIABLES_COUNTER, OPS_STACK, VARIABLES_MAPPING
    with open(f"{file_name}.rd", "r") as file_obj:
        condition_ops_length = 0
        loop_ops_length = 0
        for line in file_obj:
            if "=" in line:
                LOCAL_VARIABLES_COUNTER = assign_variable(
                    raw_line=line,
                    variables_mapping=VARIABLES_MAPPING,
                    local_variable_counter=LOCAL_VARIABLES_COUNTER,
                    ops_stack=OPS_STACK,
                    is_debug_mode=is_debug_mode,
                )
                continue

            if "++" in line:
                increment_var(
                    raw_line=line,
                    variables_mapping=VARIABLES_MAPPING,
                    ops_stack=OPS_STACK,
                    is_debug_mode=is_debug_mode,
                )
                continue

            if "show" in line:
                show_value(
                    raw_line=line,
                    variables_mapping=VARIABLES_MAPPING,
                    ops_stack=OPS_STACK,
                    is_debug_mode=is_debug_mode,
                )
                continue

            if line.startswith("condition"):
                condition_ops_length = len(OPS_STACK)
                OPS_STACK.append(line)
                continue

            if "endcondition" in line:
                condition_ops: list[str] = OPS_STACK[condition_ops_length:]
                OPS_STACK = OPS_STACK[:condition_ops_length]
                compare_values(
                    condition_ops=condition_ops,
                    variables_mapping=VARIABLES_MAPPING,
                    ops_stack=OPS_STACK,
                    is_debug_mode=is_debug_mode,
                )
                condition_ops_length = 0
                continue

            if line.startswith("loop"):
                loop_ops_length = len(OPS_STACK)
                OPS_STACK.append(line)
                continue

            if "endloop" in line:
                loop_ops: list[str] = OPS_STACK[loop_ops_length:]
                OPS_STACK = OPS_STACK[:loop_ops_length]
                run_cycle(
                    loop_ops=loop_ops,
                    variables_mapping=VARIABLES_MAPPING,
                    ops_stack=OPS_STACK,
                    is_debug_mode=is_debug_mode,
                )
                continue

    with open(f"{file_name.replace('.rd', '')}.raided", "w") as obj:
        obj.write(f"{file_name}: " + "\n")
        for op in OPS_STACK:
            obj.write("\t" + op + "\n")
    
    return f"File: {file_name.replace('.rd', '')}.raided was successfully generated.\nNum of ops: {len(OPS_STACK)}"


if __name__ == "__main__":
    compile("")
