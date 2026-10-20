```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
  parts = path_info.split("/")
  if shift > 0:
    new_script_name = f"{script_name}/{parts[0]}"
    new_path_info = "/".join(parts[1:])
  else:
    new_script_name = script_name
    new_path_info = f"{'/'.join(parts[:abs(shift)])}/{parts[abs(shift):]}"
  return new_script_name, new_path_info 
```