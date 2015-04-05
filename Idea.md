# Goal and Idea #

Mark packets with iptables so that the are routed through different GRE
Tunnels to the according (commercial) WLan Internet Service Provider (WISP).

![![](https://raw.githubusercontent.com/opencaptiveportal/opencaptiveportal/master/doc/OpenCaptivePortal_small.png)](https://raw.githubusercontent.com/opencaptiveportal/opencaptiveportal/master/doc/OpenCaptivePortal.png)

The OpenCaptivePortal Software should run on a GNU/Linux Box, which is
interconnected to a Docking Network at a University in Switzerland. See the
picture OpenCaptivePortal.png. The Box with the OpenCaptivePortal (OCP)
should achieve the ollowing objectives:

  * Acces from the Docking Network (e.g. public WLan) the selected resources
    1. VPN Router of the local University
    1. All other VPN Router of Swiss Universities as definied in the SWITCHconnect Classic ACL (Accesslist), which you can find under: https://www.switch.ch/connect/features/classic/
    1. Commercial ISPs (WISP): If a user wants to establish a connections via a WISP, he must visit the landing page of the OCP and choose a WISP. Each WISP has a iFrame on this landing page  If the user clicks on an iFrame the OCP should route all following traffic from this user through a GRE Tunnel to the specific WISP.
    1. Smart agents (like iPass) offers users the possibility to automatically connect to an WLan (for details on smart agents see [smartAgents](smartAgents.md)).
    1. Event Login, e.g. a simple login formular on the landing page where guest on events can login in (without vpn oder WISP login), see TODO.
  * IPv4 (IPv6 planned)
