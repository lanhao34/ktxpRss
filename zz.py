# -*- coding: cp936 -*-
import re
text=r'��<span class="keyword">TSDM</span>��Ļ�顿[<span class="keyword">��ħŮѧ԰</span>][Kuromajo_san_ga_Touru!!][13][<span class="keyword">720P</span>][GB����][MP4]'
print re.sub(r'(?=\<).*?(?<=>)','', text) 
