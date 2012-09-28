# -*- coding: cp936 -*-
import re
text=r'【<span class="keyword">TSDM</span>字幕组】[<span class="keyword">黑魔女学园</span>][Kuromajo_san_ga_Touru!!][13][<span class="keyword">720P</span>][GB简体][MP4]'
print re.sub(r'(?=\<).*?(?<=>)','', text) 
