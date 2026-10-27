```python
def _parse_qsl(qs: str):
    def decode(s):
        return s.replace('+', ' ').encode('latin1').decode('percent-escape')
    
    return [(decode(name), decode(value)) for segment in qs.split('&') if segment
            for name, value in [segment.split('=', 1) + [''] * (segment.count('=') == 0)]]
```