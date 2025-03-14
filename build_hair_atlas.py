import argparse
import PIL
import PIL.Image
import PIL.ImageChops

def build_hair_atlas(hair_i: PIL.Image, mask_i: PIL.Image) -> PIL.Image:
  dir_c = [
    (255, 0, 0, 255),
    (0, 255, 0, 255),
    (0, 0, 255, 255),
    (255, 0, 255, 255)
  ]

  hair_p = [(0, 0), (16, 0), (32, 0), (48, 0)]
  hair_o = [None, None, None, None]
  body_p = [[], [], [], []]

  size = mask_i.size

  mask_m = PIL.Image.new('L', size, 0)
  for y in range(mask_i.size[1]):
    for x in range(mask_i.size[0]):
      c = mask_i.getpixel((x, y))
      if c in dir_c:
        i = dir_c.index(c)
        if hair_o[i] is None:
          hair_o[i] = (x - hair_p[i][0], y - hair_p[i][1])
        o = hair_o[i]
        body_p[i].append((x - o[0], y - o[1]))
      if c[0:3] == (255, 255, 255):
        mask_m.putpixel((x, y), c[3])

  assembled_i = PIL.Image.new('RGBA', size)

  for i in range(4):
    src = (hair_p[i][0], hair_p[i][1], hair_p[i][0] + 16, hair_p[i][1] + 32)
    for x, y in body_p[i]:
      assembled_i.alpha_composite(hair_i, (x, y), src)

  masked_i = PIL.Image.new('RGBA', size)
  masked_i = PIL.Image.composite(masked_i, assembled_i, mask_m)

  return masked_i

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--hair', type=str, required=True)
  parser.add_argument('--mask', type=str, required=True)
  parser.add_argument('--output', type=str, required=True)

  args = parser.parse_args()

  hair_i = PIL.Image.open(args.hair)
  mask_i = PIL.Image.open(args.mask)

  hair_o = build_hair_atlas(hair_i, mask_i)
  hair_o.save(args.output)