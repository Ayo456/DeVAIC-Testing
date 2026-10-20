```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
  parts = path_info.split('/')
  new_script_name = script_name
  new_path_info = '/'.join(parts[shift:]) + '/' + '/'.join(parts[:shift])
  return new_script_name, new_path_info 
```