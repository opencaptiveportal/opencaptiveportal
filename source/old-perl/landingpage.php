<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<!-- 
# +-----------------------------------------------------------+
# | OpenCaptivePortal                                         |
# |                                                           |
# | For further information please see                        |
# |    https://github.com/opencaptiveportal/opencaptiveportal |
# | or                                                        |
# |    https://www.switch.ch/connect/features/pwlan/          |
# +-----------------------------------------------------------+
#
# TODO:
# - Round Robin for WISPs
-->
<html>
 <head>
  <title>SWITCH - Hotspot</title>
  <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
  <link rel="stylesheet" href="http://www.switch.ch/switch-web/css/main.css" type="text/css">
 </head>
<body bgcolor="#ffffff" topmargin="0" leftmargin="0" marginwidth="0" marginheight="0">

<!-- start header -->
<table bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" width="780">
 <tr>
  <td colspan="6"><img src="http://www.switch.ch/switch-web/images/head_spacer.gif" name="head_spacer" width="740" height="20" border="0" alt=""></td>
 </tr>
 <tr>
  <td colspan="6"><a href="http://www.switch.ch/"><img src="http://www.switch.ch/switch-web/images/start_switch_logo.gif" name="head_switch_logo" height="63" border="0" alt="SWITCH Logo"></a></td>
 </tr>
 <tr>
  <td colspan="6"><img src="http://www.switch.ch/switch-web/images/head_stripes.gif" name="head_stripes" width="780" height="15" border="0" alt=""></td>
 <tr>
  <td colspan="6"><img src="http://www.switch.ch/switch-web/images/head_colorgradient.jpg" name="head_colorgradient" width="780" height="10" border="0" alt=""></td>
 </tr>
</table>

 <!-- educational part -->
<table bgcolor="#ffffff" border="0" cellpadding="5" cellspacing="5" width="1040">
 <tr>
  <th colspan="4" align="left"><h1>Educational Internet Access</h1></th>
 </tr> 
<tr height=180>
 
 <!-- SWITCHconnect -->
 <td width=260 valign="top" bgcolor="white">
  <b>SWITCH<i>connect</i></b>
  <p><center><a href="http://www.switch.ch/mobile"><img src="http://www.switch.ch/img/Switch-connect-200.gif" border="0"></a></center><p>
  If you are a SWITCH<i>connect</i> user start up your VPN client and connect to your home campus.
 </td>
 
 <!-- local university -->
 <td width="260"  valign="top" bgcolor="white">
  <table>
   <tr>
    <td align="center">
     <b>DEINE HOCHSCHULE</b><p>
     <!-- <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BILD DER HOCHSCHULE</p> -->
     <img src="/we_want_you.jpg" /><br /><br />
     <!-- Hier koennten Informationen Deiner Hochschule bzw. des AccessPoints, von dem aus Du Dich verbindest, stehen.<br /><br /> -->
     <a href="http://www.nichtlustig.de">Link</a> zum WebVPN Deiner Hochschule. 
    </td>
   </tr>
  </table>
 </td>

 <!-- Support -->
 <td width=260  valign="top">
  <b>Support</b><p>
  In case of problems or information please contact our technical support:
  <ul>
   <li>Email: <a href="mailto:mobile@switch.ch">mobile@switch.ch</A></li>
   <li>Phone: +41 44 268 15 07</li>
  </ul>
 </td>

 <!-- Free Link -->
 <td width=260 valign="top">
  <b>Free Links</b><p>
   <ul>
    <li><a href="http://www.switch.ch">SWITCH</a></li > 
    <li><a href="http://www.sbb.ch">SBB</a> / <a href="http://www.zvv.ch">ZVV</a> / <a href="http://www.vbz.ch">VBZ</a></li>
   </ul>
  </td>
 </tr>
<!-- </table> -->

<!-- commercial part -->
<!-- TODO: Round Robin -->
<!-- <table align="left" cellpadding="5" cellspacing="5" align="left" border="1"> -->
 <tr>
  <th colspan="4" align="left"><h1>Commercial Internet Access</h1></th>
 </tr>
 <tr>
  <td>
   <!-- <a href="route.php?provider=1">TEST: KLICK HIER fuer Auswahl</a><br /><br /> -->
   <iframe src="http://iframe.monzoon.net/switch" width="261" height="200" rolling="no" frameborder="0"></iframe>
  </td>
  <td>
   <!-- <a href="route.php?provider=2">TEST: KLICK HIER fuer Auswahl</a><br /><br /> -->
   <iframe src="https://www.swisscom-mobile.ch/scm/upload/page/pwlan_roaming_iframe-en.aspx?host=taranaki.switch.ch/pwlan" width="261" height="200" rolling="no" frameborder="0"></iframe>
  </td>
  <td>
   <!-- <a href="route.php?provider=3">TEST: KLICK HIER fuer Auswahl</a><br /><br /> -->
   <iframe src="http://loginweb.tpn.ch/prelanding/switch-mobile/index.php?mpp=taranaki.switch.ch" width="261" height="200" rolling="no" frameborder="0"></iframe>
  </td>
  <td>
   <!-- <a href="route.php?provider=4">TEST: KLICK HIER fuer Auswahl</a><br /><br /> -->
   <iframe src="https://wlanauth.thenet.ch/frame/thenet_frame_secure.php?url=http://taranaki.switch.ch/&site=taranaki.switch.ch" width="261" height="200" rolling="no" frameborder="0"></iframe>
  </td>
 </tr>
</table>

<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />      
<p>
<?php
  echo "DEBUG: Deine IP Adresse: " . $_SERVER['REMOTE_ADDR'] . "\n";
?>
</p>

</body>
