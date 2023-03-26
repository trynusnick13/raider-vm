# Raider VM

![alt text](https://www.pngitem.com/pimgs/m/32-322686_oakland-raiders-logo-hd-png-download.png)
Named after Las Vegas Raiders(former Oakland Raiders)

Starting the work:

1. Install dependencies

```bash
poetry install
```

2. Choose file with `.rd` extension and compile it to the bytecode(with `.raided` extension)

```bash
python raider src/raider.py compile --no-debug-mode scripts/script_operations
```

3. Then in the folder where chosen `.rd` file located execute bytecode(interpret and execute)

```bash
python raider src/raider.py run --no-debug-mode scripts/script_operations
```

4. Additionally it is possible to compile & run together

```bash
python raider src/raider.py execute --no-debug-mode scripts/script_operations
```

## Repo structure
`scripts/` - consists of raider language scripts

`scripts/bytecode` - bytecode of the scripts with the same name and .rd extension

`src/compiler` - compiler code

`src/vm` - vm code


