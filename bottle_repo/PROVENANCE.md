# Provenance of the human-written Bottle functions

All 20 functions in `human_code/` come from a single file of a single release:

| Field | Value |
|---|---|
| Project | [Bottle](https://github.com/bottlepy/bottle) web framework |
| Release | `0.12.19` (git tag; released 2020-11-11) |
| Commit | [`152219818378926f20a5ee3d339118d7cf50a8f6`](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py) |
| File | `bottle.py` (SHA-256 `0483123aa3f8d1a9afe8b5a800f35153ab18f121510ae851a9ac89d60aea423b`) |
| License | MIT |

0.12.19 is the only release in which all 20 functions match the copies in `human_code/`.
In 0.12.18 `_parse_qsl` is different, and from 0.12.20 on `auth_basic` is different.

## How the copies were made

Each function is copied verbatim from `bottle.py`, with two changes only:
- the docstring is removed (the same step the cleaner applies to model outputs);
- methods (`_iter_chunked`, `save`) are dedented to the top level and keep their `self` parameter.

The functions call Bottle helpers (`tob`, `tonat`, `touni`, `basestring`, `DictMixin`,
`urlunquote`, `HTTPError`, `HTTPResponse`, `request`, `response`, ...), so they do not run as
standalone files. To run them in functional tests, import them from Bottle 0.12.19 itself
(`pip install bottle==0.12.19`).

## Functions and line ranges in `bottle.py` 0.12.19

| Function | Defined in | Lines |
|---|---|---|
| `_iter_chunked` | `BaseRequest` method | [1140–1165](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L1140-L1165) |
| `save` | `FileUpload` method | [2397–2414](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2397-L2414) |
| `redirect` | module | [2431–2440](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2431-L2440) |
| `_file_iter_range` | module | [2443–2450](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2443-L2450) |
| `static_file` | module | [2453–2522](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2453-L2522) |
| `http_date` | module | [2541–2548](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2541-L2548) |
| `parse_date` | module | [2550–2556](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2550-L2556) |
| `parse_auth` | module | [2558–2566](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2558-L2566) |
| `parse_range_header` | module | [2568–2584](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2568-L2584) |
| `_parse_qsl` | module | [2586–2595](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2586-L2595) |
| `_lscmp` | module | [2597–2600](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2597-L2600) |
| `cookie_encode` | module | [2603–2607](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2603-L2607) |
| `cookie_decode` | module | [2610–2617](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2610-L2617) |
| `html_escape` | module | [2625–2628](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2625-L2628) |
| `html_quote` | module | [2631–2634](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2631-L2634) |
| `yieldroutes` | module | [2637–2654](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2637-L2654) |
| `path_shift` | module (not the `BaseRequest.path_shift` method) | [2657–2685](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2657-L2685) |
| `auth_basic` | module | [2688–2700](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L2688-L2700) |
| `template` | module | [3607–3630](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L3607-L3630) |
| `view` | module | [3637–3659](https://github.com/bottlepy/bottle/blob/152219818378926f20a5ee3d339118d7cf50a8f6/bottle.py#L3637-L3659) |
