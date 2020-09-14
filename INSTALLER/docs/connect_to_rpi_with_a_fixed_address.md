# Connect to RPi with a fixed address

If you want to SSH to RPi without trouble of fluctuating IP address, you should either:

- Use RPi's [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS) domain name `raspberrypi.local` instead of IP address. Linux laptop should be installed these packages `libnss-mdns`, `avahi-daemon`, which are already pre-included in major distros (Ubuntu, Fedora).

- Configure home router to assign fixed IP for RPi (based on MAC address).

**Note**: Don't set static IP _in RPi_ itself, which makes RPi not portable.

Explanation:

If you set static IP `192.168.1.10`, for example, in RPi (_/etc/network/interfaces_ file), that RPi will not be usable when moved to other LAN network, because:

- New network may be in different subnet, `192.168.0.x`, for example.
- The RPi's static IP may be conflict with an IP managed by that network's DHCP server. DHCP server doesn't know that RPi takes `192.168.1.10`, it will try to give that IP to another client machine and that makes _both_ machines not work.

