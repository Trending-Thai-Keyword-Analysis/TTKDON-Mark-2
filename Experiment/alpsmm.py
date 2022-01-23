import re
from collections import defaultdict
from heapq import heappush, heappop  # for priority queue
from marisa_trie import Trie

wordlist = [li.strip() for li in open(r'.\words_th.txt', "r",encoding="utf-8")]
trie = Trie(wordlist)

# ช่วยตัดพวกภาษาอังกฤษ เป็นต้น
pat_eng = re.compile(r'''(?x)
[-a-zA-Z]+|   # english
\d[\d,\.]*|   # number
[ \t]+|       # space
\r?\n         # newline
''')

pat_url = re.compile(r'''(?xi)
\b
(							# Capture 1: entire matched URL
  (?:
    https?:				# URL protocol and colon
    (?:
      /{1,3}						# 1-3 slashes
      |								#   or
      [a-z0-9%]						# Single letter or digit or '%'
      								# (Trying not to match e.g. "URI::Escape")
    )
    |							#   or
    							# looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    /
  )
  (?:							# One or more:
    [^\s()<>{}\[\]]+						# Run of non-space, non-()<>{}[]
    |								#   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
  )+
  (?:							# End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
    |									#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
  )
  |					# OR, the following to match naked domains:
  (?:
  	(?<!@)			# not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    \b
    /?
    (?!@)			# not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
  )
)''')

# TCC
pat_tcc = """\
เcอร์
เc็c
เcctาะ
เccีtยะ
เccีtย(?=[เ-ไก-ฮ]|$)
เccอะ
เcc็c
เcิc์c
เcิtc
เcีtยะ?
เcืtอะ?
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)
เctา?ะ?
cัtวะ
c[ัื]tc[ุิะ]?
c[ิุู]์
c[ะ-ู]t
c็
ct[ะาำ]?
แc็c
แcc์
แctะ
แcc็c
แccc์
โctะ
[เ-ไ]ct
""".replace('c','[ก-ฮ]').replace('t', '[่-๋]?').split()
# print(pat_tcc)
# print("|".join(pat_tcc))

def tcc(w):
    p = 0
    pat = re.compile("|".join(pat_tcc))
    while p<len(w):
        m = pat.match(w[p:])
        if m:
            # print(m.group())
            n = m.span()[1]
        else:
            # print(m)
            n = 1
        # print(w[p:p+n])
        yield w[p:p+n]
        p += n

def tcc_pos(text):
    p_set = set()
    p = 0
    # print(tcc(text))
    for w in tcc(text):
        # print(w)
        p += len(w)
        p_set.add(p)
    # print(p_set)
    return p_set

def serialize(words_at, p, p2):   
  # find path ทั้งหมด แบบ depth first
  if p in words_at:
    for w in words_at[p]:
      p_ = p + len(w)
      if p_== p2:
        yield [w]
      elif p_ < p2:
        for path in serialize(words_at, p_, p2):
          yield [w]+path

def onecut(text,keepwhitespace):
  words_at = defaultdict(list)  # main data structure
  # print(dict(words_at))
  allow_pos = tcc_pos(text)     # ตำแหน่งที่ตัด ต้องตรงกับ tcc
  # print(allow_pos)
  q = [0]       # min-heap queue
  last_p = 0    # last position for yield
  while q[0] < len(text):
      # print(q)
      p = heappop(q)
      # print(p,q)

      # print(text[p:])
      # print(trie.prefixes(text[p:]))
      for w in trie.prefixes(text[p:]):
          # print(text[p:])
          p_ = p + len(w)
          # print(p_)
          if p_ in allow_pos:  # เลือกที่สอดคล้อง tcc
            words_at[p].append(w)
            # print(dict(words_at))
            if p_ not in q:
              heappush(q, p_)   

      # กรณี length 1 คือ ไม่กำกวมแล้ว ส่งผลลัพธ์ก่อนนี้คืนได้
      if len(q)==1:
          # print(dict(words_at))
          paths = serialize(words_at, last_p, q[0])
          # print(list(serialize(words_at, last_p, q[0])))
          for w in min(paths, key=len):
            # print(w)
            if keepwhitespace or not w.isspace():
              yield w
          last_p = q[0]

      # กรณี length 0  คือ ไม่มีใน dict
      if len(q)==0:
          m = pat_eng.match(text[p:])
          n = pat_url.match(text[p:])
          if n:
              # print(n.group())
              i = p + n.end()
          elif m: # อังกฤษ, เลข, ว่าง
              # print(m.end())
              # print("match " +m.group())
              i = p + m.end()
          else: # skip น้อยที่สุด ที่เป็นไปได้
              for i in range(p+1, len(text)):
                  if i in allow_pos:   # ใช้ tcc ด้วย ทั้งจุดเริ่มและจบ
                      ww = [w for w in trie.prefixes(text[i:]) if (i+len(w) in allow_pos)]
                      # print(ww)
                      m = pat_eng.match(text[i:])
                      # print(m)
                      if ww or m:
                          break
              else:
                  i = len(text)
          # print(i)
          w = text[p:i]
          if keepwhitespace or not w.isspace():
            words_at[p].append(w)
            # print(dict(words_at))
            yield w
          last_p = i
          heappush(q, i)
          
# ช่วยให้ไม่ต้องพิมพ์ยาวๆ
def mmcut(text,keep_whitespace=True):
  return list(onecut(text,keep_whitespace))
