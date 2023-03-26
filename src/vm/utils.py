def extract_all_commands(file_name: str) -> list[str]:
    """
    Reading file with raider bytecode and deleting comments with extra spaces

    :param file_name: name of the file to process
    :return: list of all ops
    """
    ops_commands = []
    with open(f"{file_name}.raided", "r") as file_obj:
        for counter, line in enumerate(file_obj):
            if counter == 0:
                continue # skipping first line with script file_name
            if "--" in line:
                ops_commands.append("empty")
                continue
            prepared_op = line.strip()
            ops_commands.append(prepared_op)
    
    return ops_commands
