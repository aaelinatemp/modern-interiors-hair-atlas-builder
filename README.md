### Usage
```
python build_hair_atlas.py --hair hair.png --mask mask_short.png --output hair_atlas.png
```

`mask_short.png` is for hair that stops at the shoulders (all existing hair). `mask_long.png` has extra masking so that all down facing arm actions are visible. Expecting sprites in the layout of `hair.png` 

Requires Pillow. `pip install pillow`
