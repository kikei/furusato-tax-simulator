class Sheet(object):
  VALUE = 0
  CAPTION = 1

  def __init__(self):
    self.items = []
    self.keys = set()

  def __getitem__(self, key):
    if key in self.keys:
      for ty, k, item in self.items:
        if ty == Sheet.VALUE and k == key:
          return item
    raise KeyError(key)

  def __setitem__(self, key, item):
    if key in self.keys:
      for i in range(0, len(self.items)):
        if self.items[i][0] == key:
          self.items[i][1] = item
          return
      raise KeyError(key)
    else:
      self.items.append((Sheet.VALUE, key, item))
      self.keys.add(key)

  def __str__(self):
    lines = []
    for ty, key, item in self.items:
      if ty == Sheet.VALUE:
        if item < 1.0:
          lines.append('{k}\t\t{v:.4f}'.format(k=key, v=item))
        else:
          lines.append('{k}\t\t{v:7,.0f}'.format(k=key, v=item))
      elif ty == Sheet.CAPTION:
        lines.append('# {k}'.format(k=key))
    return '\n'.join(lines)

  def addCaption(self, caption):
    self.items.append((Sheet.CAPTION, caption, None))

x = Sheet()
x['給与収入'] = 6600001
x['所得控除計(寄付金控除以外)'] = 134871
x['ふるさと納税寄付額'] = 120000
x['人的控除差額'] = 0

x.addCaption('所得')
assert 6600000 < x['給与収入'] < 10000000
x['給与所得'] = x['給与収入'] * 0.9 - 1200000
x['給与所得控除'] = x['給与収入'] * 0.1 + 1200000

x['寄付金控除'] = x['ふるさと納税寄付額']
x['所得控除計'] = x['所得控除計(寄付金控除以外)'] + x['寄付金控除']
x['課税標準額'] = x['給与所得'] - x['所得控除計']
assert 3300000 < x['課税標準額'] < 6950000
x['所得控除額'] = 427500
x['所得税率'] = 0.20
x['所得税額'] = x['課税標準額'] * x['所得税率'] - x['所得控除額']
x['復興特別所得税率'] = x['所得税率'] * 0.021

x.addCaption('住民税')
x['所得割額(都民税)'] = x['課税標準額'] * 0.04
x['所得割額(特別区民税)'] = x['課税標準額'] * 0.06
x['所得割額経計'] = x['所得割額(都民税)'] + x['所得割額(特別区民税)']
x['調整控除額(都民税)'] = max(50000, x['所得割額(都民税)'] - 2000000) * 0.02
x['調整控除額(特別区民税)'] = max(50000, x['所得割額(特別区民税)'] - 2000000) * 0.03
x['調整控除後所得割(都民税)'] = x['所得割額(都民税)'] - x['調整控除額(都民税)']
x['調整控除後所得割(特別区民税)'] = \
  x['所得割額(特別区民税)'] - x['調整控除額(特別区民税)']
x['調整控除後所得割計'] = \
  x['調整控除後所得割(都民税)'] + x['調整控除後所得割(特別区民税)']
x['均等割額(都民税)'] = 1500
x['均等割額(特別区民税)'] = 3500
x['住民税額(都民税)'] = x['調整控除後所得割(都民税)'] + x['均等割額(都民税)']
x['住民税額(特別区民税)'] = \
  x['調整控除後所得割(特別区民税)'] + x['均等割額(特別区民税)']
x['住民税額計'] = x['住民税額(都民税)'] + x['住民税額(特別区民税)']

x.addCaption('ふるさと納税')
x['所得税からの控除額'] = \
  (x['ふるさと納税寄付額'] - 2000) * (x['所得税率'] + x['復興特別所得税率'])
x['寄付金控除(基本分)'] = \
  (x['ふるさと納税寄付額'] - 2000) * 0.1
x['寄付金控除(特例分)'] = \
  (x['ふるさと納税寄付額'] - 2000) * (0.9 - x['所得税率'] - x['復興特別所得税率'])
assert x['寄付金控除(特例分)'] < x['調整控除後所得割計'] * 0.2

x['ふるさと納税控除額'] = \
  x['所得税からの控除額'] + x['寄付金控除(基本分)'] + x['寄付金控除(特例分)']

print(x)
