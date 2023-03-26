from enum import IntEnum

import yaml
import os

with open("compiler/commands_config.yml", "r") as data_stream:
    CONFIG = yaml.safe_load(data_stream)

COMMANDS = CONFIG["bytecode_commands"]
LOCAL_VARIABLES_COUNTER = 0
OPS_STACK = []
VARIABLES_MAPPING = {}
DEBUG_MODE = os.getenv("DEBUG_MODE", True)


class Assignment(IntEnum):
    NAME = 0
    VALUE = 1


class Operator(IntEnum):
    NAME = 0
    VALUE = 1


class Compare(IntEnum):
    LEFT = 0
    RIGHT = 1


def add_values(
    raw_summands: str,
    variables_mapping: dict[str, int],
    ops_stack: list[str],
):
    ops_stack.append("--- Addition Starting ---")
    summands: list[str] = raw_summands.split("+")
    summands = [summand.strip() for summand in summands]
    for summand in summands:
        if not summand.isdigit():
            local_var_idx = variables_mapping[summand]
            command = (
                f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {local_var_idx}"
            )
        else:
            command = f"{COMMANDS['LOAD_VALUE_TO_STACK']['name']} {summand}"
        ops_stack.append("\t" + command)

    command = f"{COMMANDS['ADD_VALUES']['name']} {len(summands)}"
    ops_stack.append("\t" + command)
    ops_stack.append("--- Addition Finished ---")


def mult_values(
    raw_multipliers: str,
    variables_mapping: dict[str, int],
    ops_stack: list[str],
):
    ops_stack.append("--- Multiplication Starting ---")
    multipliers: list[str] = raw_multipliers.split("*")
    multipliers = [summand.strip() for summand in multipliers]
    for multiplier in multipliers:
        if not multiplier.isdigit():
            local_var_idx = variables_mapping[multiplier]
            command = (
                f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {local_var_idx}"
            )
        else:
            command = f"{COMMANDS['LOAD_VALUE_TO_STACK']['name']} {multiplier}"
        ops_stack.append("\t" + command)

    command = f"{COMMANDS['MULT_VALUES']['name']} {len(multipliers)}"
    ops_stack.append("\t" + command)
    ops_stack.append("--- Multiplication Finished ---")


def assign_variable(
    raw_line: str,
    variables_mapping: dict[str, int],
    local_variable_counter: int,
    ops_stack: list[str],
    is_debug_mode: bool = False,
) -> int:
    assignment_pair = raw_line.split("=")
    var_name = assignment_pair[Assignment.NAME].strip()
    var_value = assignment_pair[Assignment.VALUE].strip()
    if "+" in var_value:
        add_values(
            raw_summands=var_value,
            variables_mapping=variables_mapping,
            ops_stack=ops_stack,
        )
    elif "*" in var_value:
        mult_values(
            raw_multipliers=var_value,
            variables_mapping=variables_mapping,
            ops_stack=ops_stack,
        )
    else:
        command = f"{COMMANDS['LOAD_VALUE_TO_STACK']['name']} {var_value}"
        ops_stack.append(command)

    var_idx = variables_mapping.get(var_name)
    if var_idx is not None:
        command = f"{COMMANDS['LOAD_VALUE_TO_LOCAL_VARIABLE_ARRAY']['name']} {var_idx}"
    else:
        variables_mapping[var_name] = local_variable_counter
        command = (
            f"{COMMANDS['LOAD_VALUE_TO_LOCAL_VARIABLE_ARRAY']['name']} {local_variable_counter}"
        )
        local_variable_counter += 1
    ops_stack.append(command)

    return local_variable_counter


def increment_var(
    raw_line: str,
    variables_mapping: dict[str, int],
    ops_stack: list[str],
    is_debug_mode: bool = False,
):
    var_name = raw_line.strip("\n").strip("+")
    if is_debug_mode:
        print(var_name)
    local_var_idx = variables_mapping[var_name]
    command = f"{COMMANDS['INC_VALUE']['name']} {local_var_idx}"

    ops_stack.append(command)


def show_value(
    raw_line: str,
    variables_mapping: dict[str, int],
    ops_stack: list[str],
    is_debug_mode: bool = False,
):
    ops_stack.append("--- Printing Starting ---")
    operator_pair = raw_line.strip().split(" ")
    op_value = operator_pair[Operator.VALUE].strip()
    if is_debug_mode:
        print(op_value)
        print(variables_mapping)
        print(operator_pair)
    local_var_idx = variables_mapping[op_value]
    command = f"{COMMANDS['PRINT_VALUE']['name']} {local_var_idx}"
    ops_stack.append(command)
    ops_stack.append("--- Printing Finished ---")


def compare_values(
    condition_ops: list[str],
    variables_mapping: dict[str, int],
    ops_stack: list[str],
    is_debug_mode: bool = False,
):
    condition_line = condition_ops.pop(0)

    if "<" in condition_line:
        condition_line = condition_line.replace("condition", "")
        comparators_pair = condition_line.split("<")
        left_cmp = comparators_pair[Compare.LEFT].strip()
        right_cmp = comparators_pair[Compare.RIGHT].strip()
        left_idx = variables_mapping[left_cmp]
        right_idx = variables_mapping[right_cmp]
        ops_stack.append("--- Condition Starting ---")
        ops_stack.append(
            f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {left_idx}"
        )
        ops_stack.append(
            f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {right_idx}"
        )
        ops_stack.append(f"{COMMANDS['LESS_THAN']['name']}")
        ops_stack.append(f"{COMMANDS['FORWARD_JUMP']['name']} {len(condition_ops)}")
        ops_stack.extend(condition_ops)
        ops_stack.append("--- Condition Finished ---")


def run_cycle(
    loop_ops: list[str],
    variables_mapping: dict[str, int],
    ops_stack: list[str],
    is_debug_mode: bool = False,
):
    condition_line = loop_ops.pop(0)

    if "<" in condition_line:
        condition_line = condition_line.replace("loop", "")
        comparators_pair = condition_line.split("<")
        left_cmp = comparators_pair[Compare.LEFT].strip()
        right_cmp = comparators_pair[Compare.RIGHT].strip()
        left_idx = variables_mapping[left_cmp]
        right_idx = variables_mapping[right_cmp]
        ops_stack.append("--- Loop Starting ---")
        ops_stack.append(
            f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {left_idx}"
        )
        ops_stack.append(
            f"{COMMANDS['LOAD_VALUE_FROM_LOCAL_VARIABLE_ARRAY']['name']} {right_idx}"
        )
        ops_stack.append(f"{COMMANDS['LESS_THAN']['name']}")
        ops_stack.append(f"{COMMANDS['FORWARD_JUMP']['name']} {len(loop_ops) + 1}")
        ops_stack.extend(loop_ops)
        ops_stack.append(f"{COMMANDS['BACK_JUMP']['name']} {len(loop_ops) + 4}")
        ops_stack.append("--- Loop Finished ---")
