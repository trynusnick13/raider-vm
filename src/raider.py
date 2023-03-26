import typer

from compiler import compiler
from vm import vm

app = typer.Typer()


@app.command()
def compile_to_raider_bytecode(file_name: str, debug_mode: bool = False) -> str:
    """
    Compiles <file_name>.rd file and generates  <file_name>.raided file with bytecode

    :param file_name: name of the file to compile
    """
    generated_file_name: str = compiler.compile(file_name, debug_mode)
    print(generated_file_name)

    return generated_file_name

@app.command()
def run_raider_bytecode(file_name: str, debug_mode: bool = False):
    """
    Runs <file_name>.raided file with bytecode

    :param file_name: name of the file to execute
    """
    vm.run_bytecode(file_name, debug_mode)

@app.command()
def compile_and_run(file_name: str, is_debug_mode: bool = False):
    compiler.compile(file_name, is_debug_mode)
    vm.run_bytecode(file_name, is_debug_mode)


if __name__ == "__main__":
    app()
