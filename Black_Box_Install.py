#! /usr/bin/env python3

import os

wifi = input('Are you connected to WiFi?[y/N]: ')
if wifi == 'y' or wifi == 'Y':
  print('[*]Continuing Setup...')
else:
  print('[*]Please connect to WiFi before setting up RPi Black Box.')
  exit()

user = input('Are you using default user pi?[y/N]: ')
if user == 'y' or user == 'Y':
  print('[*]Continuing Setup...')
else:
  print('[*]Please login as pi or recreate user pi.')
  exit()

os.system('sudo apt-get update && sudo apt-get upgrade')
os.system('sudo apt-get install motion gpac ssh samba samba-common-bin hostpad dnsmasq apache2 aircrack-ng -y')

os.system('sudo mkdir /home/pi/.motion')
os.system('sudo mkdir /home/pi/PARKED')
os.system('sudo mkdir /home/pi/DRIVING')
os.system('sudo mkdir /home/pi/BB_NETWORK')

os.chdir('/etc')

with open('dhcpcd.conf', 'a+') as f:
  f.write('denyinterfaces wlan0')
f.close()

os.chdir('network/')

interfaces = """\
auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet static
address 192.168.1.2
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 8.8.8.8 8.8.4.4

allow-hotplug wlan0
iface wlan0 inet static
address 192.168.220.1
netmask 255.255.255.0
network 192.168.220.0
broadcast 192.168.220.255
# wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
"""

with open('interfaces', 'a+') as f:
  f.write(interfaces)
f.close()

os.chdir('/home/pi/BB_NETWORK')

hostapd = """\
# WifI interface and driver to be used
interface=wlan0
driver=nl80211

# WiFi settings
hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=1
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
macaddr_acl=0
ignore_broadcast_ssid=0

# Use WPA authentication and a pre-shared key
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# Network Name
ssid=BlackBox
# Network password
wpa_passphrase=raspberry
"""

with open('hostapd.conf', 'w+') as f:
  f.write(hostapd)
f.close()

os.chdir('/home/pi/.motion')

#/etc/samba/smb.conf
smb = """\
[PARKED]
path = /home/pi/PARKED
writeable=Yes
create mask=0777
directory mask=0777
public=no

[DRIVING]
path = /home/pi/DRIVING
writeable=Yes
create mask=0777
directory mask=0777
public=no
"""

#/etc/ssh/sshd_config
sshd_config = """\
# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/usr/bin:/bin:/usr/sbin:/sbin

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default value.

Protocol 2

Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
#LogLevel INFO

# Authentication:

#LoginGraceTime 2m
PermitRootLogin no
#StrictModes yes
MaxAuthTries 10
#MaxSessions 10

PubkeyAuthentication yes

# Expect .ssh/authorized_keys2 to be disregarded by default in future.
#AuthorizedKeysFile     .ssh/authorized_keys .ssh/authorized_keys2

#AuthorizedPrincipalsFile none

#AuthorizedKeysCommand none
#AuthorizedKeysCommandUser nobody

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
PermitEmptyPasswords no

# Change to yes to enable challenge-response passwords (beware issues with
# some PAM modules and threads)
ChallengeResponseAuthentication no

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no

# GSSAPI options
#GSSAPIAuthentication no
#GSSAPICleanupCredentials yes
#GSSAPIStrictAcceptorCheck yes
#GSSAPIKeyExchange no

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# the setting of PermitRootLogin without-password.
# If you just want the PAM account and session checks to run without
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
UsePAM yes

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
X11Forwarding no
#X11DisplayOffset 10
#X11UseLocalhost yes
#PermitTTY yes
PrintMotd no
#PrintLastLog yes
#TCPKeepAlive yes
#PermitUserEnvironment no
#Compression delayed
ClientAliveInterval 300
#ClientAliveCountMax 3
#UseDNS no
#PidFile /var/run/sshd.pid
#MaxStartups 10:30:100
#PermitTunnel no
#ChrootDirectory none
#VersionAddendum none

# no default banner path
#Banner none

# Allow client to pass locale environment variables
AcceptEnv LANG LC_*

# override default of no subsystems
Subsystem       sftp    /usr/lib/openssh/sftp-server

# Example of overriding settings on a per-user basis
#Match User anoncvs
#       X11Forwarding no
#       AllowTcpForwarding no
#       PermitTTY no
#       ForceCommand cvs server
"""

#/etc/default/motion
daemon = "start_motion_daemon = yes" 

#~/.motion/parked.conf
parked = """\ 
# Motion for Pi project - main conf.
# This config file was generated by motion 4.0
#
# Author: @greenido
#
# Date: 10/2018
#
# See: https://greenido.wordpress.com/?p=9397
#
# IMPORTANT: Please search after TODO and make sure you change them with your settings.
#
############################################################
# Daemon
############################################################
# Start in daemon (background) mode and release terminal (default: off)
daemon on

# File to store the process ID, also called pid file. (default: not defined)
process_id_file /var/run/motion/motion.pid

############################################################
# Basic Setup Mode
############################################################

# Start in Setup-Mode, daemon disabled. (default: off)
setup_mode off

# Use a file to save logs messages, if not defined stderr and syslog is used. (default: not defined)
logfile /home/pi/.motion/motion.log

# Level of log messages [1..9] (EMG, ALR, CRT, ERR, WRN, NTC, INF, DBG, ALL). (default: 6 / NTC)
log_level 7

# Filter to log messages by type (COR, STR, ENC, NET, DBL, EVT, TRK, VID, ALL). (default: ALL)
log_type all

###########################################################
# Capture device options
############################################################

# Videodevice to be used for capturing  (default /dev/video0)
# for FreeBSD default is /dev/bktr0
videodevice /dev/video0

# v4l2_palette allows one to choose preferable palette to be use by motion
# to capture from those supported by your videodevice. (default: 17)
# E.g. if your videodevice supports both V4L2_PIX_FMT_SBGGR8 and
# V4L2_PIX_FMT_MJPEG then motion will by default use V4L2_PIX_FMT_MJPEG.
# Setting v4l2_palette to 2 forces motion to use V4L2_PIX_FMT_SBGGR8
# instead.
#
# Values :
# V4L2_PIX_FMT_SN9C10X : 0  'S910'
# V4L2_PIX_FMT_SBGGR16 : 1  'BYR2'
# V4L2_PIX_FMT_SBGGR8  : 2  'BA81'
# V4L2_PIX_FMT_SPCA561 : 3  'S561'
# V4L2_PIX_FMT_SGBRG8  : 4  'GBRG'
# V4L2_PIX_FMT_SGRBG8  : 5  'GRBG'
# V4L2_PIX_FMT_PAC207  : 6  'P207'
# V4L2_PIX_FMT_PJPG    : 7  'PJPG'
# V4L2_PIX_FMT_MJPEG   : 8  'MJPEG'
# V4L2_PIX_FMT_JPEG    : 9  'JPEG'
# V4L2_PIX_FMT_RGB24   : 10 'RGB3'
# V4L2_PIX_FMT_SPCA501 : 11 'S501'
# V4L2_PIX_FMT_SPCA505 : 12 'S505'
# V4L2_PIX_FMT_SPCA508 : 13 'S508'
# V4L2_PIX_FMT_UYVY    : 14 'UYVY'
# V4L2_PIX_FMT_YUYV    : 15 'YUYV'
# V4L2_PIX_FMT_YUV422P : 16 '422P'
# V4L2_PIX_FMT_YUV420  : 17 'YU12'
#
v4l2_palette 17

# Tuner device to be used for capturing using tuner as source (default /dev/tuner0)
# This is ONLY used for FreeBSD. Leave it commented out for Linux
; tunerdevice /dev/tuner0

# The video input to be used (default: -1)
# Should normally be set to 0 or 1 for video/TV cards, and -1 for USB cameras
# Set to 0 for uvideo(4) on OpenBSD
input -1

# The video norm to use (only for video capture and TV tuner cards)
# Values: 0 (PAL), 1 (NTSC), 2 (SECAM), 3 (PAL NC no colour). Default: 0 (PAL)
norm 0

# The frequency to set the tuner to (kHz) (only for TV tuner cards) (default: 0)
frequency 0

# Override the power line frequency for the webcam. (normally not necessary)
# Values: 
# -1 : Do not modify device setting
# 0  : Power line frequency Disabled
# 1  : 50hz
# 2  : 60hz
# 3  : Auto
power_line_frequency -1

# Rotate image this number of degrees. The rotation affects all saved images as
# well as movies. Valid values: 0 (default = no rotation), 90, 180 and 270.
rotate 0

# Image width (pixels). Valid range: Camera dependent, default: 352
width 640

# Image height (pixels). Valid range: Camera dependent, default: 288
height 480

# Maximum number of frames to be captured per second.
# Valid range: 2-100. Default: 100 (almost no limit).
framerate 60

# Minimum time in seconds between capturing picture frames from the camera.
# Default: 0 = disabled - the capture rate is given by the camera framerate.
# This option is used when you want to capture images at a rate lower than 2 per second.
minimum_frame_time 0

# URL to use if you are using a network camera, size will be autodetected (incl http:// ftp:// mjpg:// rtsp:// mjpeg:// or file:///)
# Must be a URL that returns single jpeg pictures or a raw mjpeg stream. A trailing slash may be required for some cameras.
# Default: Not defined
; netcam_url value

# Username and password for network camera (only if required). Default: not defined
# Syntax is user:password
; netcam_userpass value

# The setting for keep-alive of network socket, should improve performance on compatible net cameras.
# off:   The historical implementation using HTTP/1.0, closing the socket after each http request.
# force: Use HTTP/1.0 requests with keep alive header to reuse the same connection.
# on:    Use HTTP/1.1 requests that support keep alive as default.
# Default: off
netcam_keepalive off

# URL to use for a netcam proxy server, if required, e.g. "http://myproxy".
# If a port number other than 80 is needed, use "http://myproxy:1234".
# Default: not defined
; netcam_proxy value

# Set less strict jpeg checks for network cameras with a poor/buggy firmware.
# Default: off
netcam_tolerant_check off

# RTSP connection uses TCP to communicate to the camera. Can prevent image corruption.
# Default: on
rtsp_uses_tcp on

# Name of camera to use if you are using a camera accessed through OpenMax/MMAL
# Default: Not defined
mmalcam_name vc.ril.camera

# Camera control parameters (see raspivid/raspistill tool documentation)
# Default: Not defined
; mmalcam_control_params -hf

# Let motion regulate the brightness of a video device (default: off).
# The auto_brightness feature uses the brightness option as its target value.
# If brightness is zero auto_brightness will adjust to average brightness value 128.
# Only recommended for cameras without auto brightness
auto_brightness off

# Set the initial brightness of a video device.
# If auto_brightness is enabled, this value defines the average brightness level
# which Motion will try and adjust to.
# Valid range 0-255, default 0 = disabled
brightness 0

# Set the contrast of a video device.
# Valid range 0-255, default 0 = disabled
contrast 0

# Set the saturation of a video device.
# Valid range 0-255, default 0 = disabled
saturation 0

# Set the hue of a video device (NTSC feature).
# Valid range 0-255, default 0 = disabled
hue 0


############################################################
# Round Robin (multiple inputs on same video device name)
############################################################

# Number of frames to capture in each roundrobin step (default: 1)
roundrobin_frames 1

# Number of frames to skip before each roundrobin step (default: 1)
roundrobin_skip 1

# Try to filter out noise generated by roundrobin (default: off)
=switchfilter off


############################################################
# Motion Detection Settings:
############################################################

# Threshold for number of changed pixels in an image that
# triggers motion detection (default: 1500) - 
# TODO: try few number to reduce the false/positives ratio
#
threshold 2500

# Automatically tune the threshold down if possible (default: off)
threshold_tune off

# Noise threshold for the motion detection (default: 32)
noise_level 32

# Automatically tune the noise threshold (default: on)
noise_tune on

# Despeckle motion image using (e)rode or (d)ilate or (l)abel (Default: not defined)
# Recommended value is EedDl. Any combination (and number of) of E, e, d, and D is valid.
# (l)abeling must only be used once and the 'l' must be the last letter.
# Comment out to disable
despeckle_filter EedDl

# Detect motion in predefined areas (1 - 9). Areas are numbered like that:  1 2 3
# A script (on_area_detected) is started immediately when motion is         4 5 6
# detected in one of the given areas, but only once during an event.        7 8 9
# One or more areas can be specified with this option. Take care: This option
# does NOT restrict detection to these areas! (Default: not defined)
; area_detect 4,5,6

# PGM file to use as a sensitivity mask.
# Full path name to. (Default: not defined)
; mask_file value

# Dynamically create a mask file during operation (default: 0)
# Adjust speed of mask changes from 0 (off) to 10 (fast)
smart_mask_speed 0

# Ignore sudden massive light intensity changes given as a percentage of the picture
# area that changed intensity. Valid range: 0 - 100 , default: 0 = disabled
lightswitch 0

# Picture frames must contain motion at least the specified number of frames
# in a row before they are detected as true motion. At the default of 1, all
# motion is detected. Valid range: 1 to thousands, recommended 1-5
minimum_motion_frames 4

# Specifies the number of pre-captured (buffered) pictures from before motion
# was detected that will be output at motion detection.
# Recommended range: 0 to 5 (default: 0)
# Do not use large values! Large values will cause Motion to skip video frames and
# cause unsmooth movies. To smooth movies use larger values of post_capture instead.
pre_capture 0

# Number of frames to capture after motion is no longer detected (default: 0)
post_capture 0

# Event Gap is the seconds of no motion detection that triggers the end of an event.
# An event is defined as a series of motion images taken within a short timeframe.
# Recommended value is 60 seconds (Default). The value -1 is allowed and disables
# events causing all Motion to be written to one single movie file and no pre_capture.
# If set to 0, motion is running in gapless mode. Movies don't have gaps anymore. An
# event ends right after no more motion is detected and post_capture is over.
event_gap 15

# Maximum length in seconds of a movie
# When value is exceeded a new movie file is created. (Default: 0 = infinite)
max_movie_time 0

# Always save images even if there was no motion (default: off)
emulate_motion off

############################################################
# Image File Output
############################################################

# Output 'normal' pictures when motion is detected (default: on)
# Valid values: on, off, first, best, center
# When set to 'first', only the first picture of an event is saved.
# Picture with most motion of an event is saved when set to 'best'.
# Picture with motion nearest center of picture is saved when set to 'center'.
# Can be used as preview shot for the corresponding movie.
output_pictures normal

# Output pictures with only the pixels moving object (ghost images) (default: off)
output_debug_pictures off

# The quality (in percent) to be used by the jpeg compression (default: 75)
quality 80

# Type of output images
# Valid values: jpeg, ppm (default: jpeg)
picture_type jpeg

############################################################
# FFMPEG related options
# Film (movies) file output, and deinterlacing of the video input
# The options movie_filename and timelapse_filename are also used
# by the ffmpeg feature
############################################################

# Use ffmpeg to encode movies in realtime (default: off)
ffmpeg_output_movies off

# Use ffmpeg to make movies with only the pixels moving
# object (ghost images) (default: off)
ffmpeg_output_debug_movies off

# Use ffmpeg to encode a timelapse movie
# Default value 0 = off - else save frame every Nth second
ffmpeg_timelapse 0

# The file rollover mode of the timelapse video
# Valid values: hourly, daily (default), weekly-sunday, weekly-monday, monthly, manual
ffmpeg_timelapse_mode daily

# Bitrate to be used by the ffmpeg encoder (default: 400000)
# This option is ignored if ffmpeg_variable_bitrate is not 0 (disabled)
ffmpeg_bps 400000

# Enables and defines variable bitrate for the ffmpeg encoder.
# ffmpeg_bps is ignored if variable bitrate is enabled.
# Valid values: 0 (default) = fixed bitrate defined by ffmpeg_bps,
# or the range 1 - 100 where 1 means worst quality and 100 is best.
ffmpeg_variable_bitrate 0

# Codec to used by ffmpeg for the video compression.
# Timelapse videos have two options.
#   mpg - Creates mpg file with mpeg-2 encoding.
#     If motion is shutdown and restarted, new pics will be appended
#     to any previously created file with name indicated for timelapse.
#   mpeg4 - Creates avi file with the default encoding.
#     If motion is shutdown and restarted, new pics will create a
#     new file with the name indicated for timelapse.
# Supported formats are:
# mpeg4 or msmpeg4 - gives you files with extension .avi
# msmpeg4 is recommended for use with Windows Media Player because
# it requires no installation of codec on the Windows client.
# swf - gives you a flash film with extension .swf
# flv - gives you a flash video with extension .flv
# ffv1 - FF video codec 1 for Lossless Encoding
# mov - QuickTime
# mp4 - MPEG-4 Part 14 H264 encoding
# mkv - Matroska H264 encoding
# hevc - H.265 / HEVC (High Efficiency Video Coding)
ffmpeg_video_codec mpeg4

# When creating videos, should frames be duplicated in order 
# to keep up with the requested frames per second
# (default: true)
ffmpeg_duplicate_frames true

############################################################
# SDL Window
############################################################

# Number of motion thread to show in SDL Window (default: 0 = disabled)
#sdl_threadnr 0

############################################################
# External pipe to video encoder
# Replacement for FFMPEG builtin encoder for ffmpeg_output_movies only.
# The options movie_filename and timelapse_filename are also used
# by the ffmpeg feature
#############################################################

# Bool to enable or disable extpipe (default: off)
use_extpipe off

# External program (full path and opts) to pipe raw video to
# Generally, use '-' for STDIN...
;extpipe mencoder -demuxer rawvideo -rawvideo w=%w:h=%h:i420 -ovc x264 -x264encopts bframes=4:frameref=1:subq=1:scenecut=-1:nob_adapt:threads=1:keyint=1000:8x8dct:vbv_bufsize=4000:crf=24:partitions=i8x8,i4x4:vbv_maxrate=800:no-chroma-me -vf denoise3d=16:12:48:4,pp=lb -of   avi -o %f.avi - -fps %fps
;extpipe x264 - --input-res %wx%h --fps %fps --bitrate 2000 --preset ultrafast --quiet -o %f.mp4
;extpipe mencoder -demuxer rawvideo -rawvideo w=%w:h=%h:fps=%fps -ovc x264 -x264encopts preset=ultrafast -of lavf -o %f.mp4 - -fps %fps
;extpipe ffmpeg -y -f rawvideo -pix_fmt yuv420p -video_size %wx%h -framerate %fps -i pipe:0 -vcodec libx264 -preset ultrafast -f mp4 %f.mp4


############################################################
# Snapshots (Traditional Periodic Webcam File Output)
############################################################

# Make automated snapshot every N seconds (default: 0 = disabled)
snapshot_interval 0


############################################################
# Text Display
# %Y = year, %m = month, %d = date,
# %H = hour, %M = minute, %S = second, %T = HH:MM:SS,
# %v = event, %q = frame number, %t = camera id number,
# %D = changed pixels, %N = noise level, \n = new line,
# %i and %J = width and height of motion area,
# %K and %L = X and Y coordinates of motion center
# %C = value defined by text_event - do not use with text_event!
# You can put quotation marks around the text to allow
# leading spaces
############################################################

# Locate and draw a box around the moving object.
# Valid values: on, off, preview (default: off)
# Set to 'preview' will only draw a box in preview_shot pictures.
locate_motion_mode on

# Set the look and style of the locate box if enabled.
# Valid values: box, redbox, cross, redcross (default: box)
# Set to 'box' will draw the traditional box.
# Set to 'redbox' will draw a red box.
# Set to 'cross' will draw a little cross to mark center.
# Set to 'redcross' will draw a little red cross to mark center.
locate_motion_style box

# Draws the timestamp using same options as C function strftime(3)
# Default: %Y-%m-%d\n%T = date in ISO format and time in 24 hour clock
# Text is placed in lower right corner
text_right %Y-%m-%d\n%T-%q

# Draw a user defined text on the images using same options as C function strftime(3)
# Default: Not defined = no text
# Text is placed in lower left corner
; text_left CAMERA %t

# Draw the number of changed pixed on the images (default: off)
# Will normally be set to off except when you setup and adjust the motion settings
# Text is placed in upper right corner
text_changes on

# This option defines the value of the special event conversion specifier %C
# You can use any conversion specifier in this option except %C. Date and time
# values are from the timestamp of the first image in the current event.
# Default: %Y%m%d%H%M%S
# The idea is that %C can be used filenames and text_left/right for creating
# a unique identifier for each event.
text_event %Y%m%d%H%M%S

# Draw characters at twice normal size on images. (default: off)
text_double off


# Text to include in a JPEG EXIF comment
# May be any text, including conversion specifiers.
# The EXIF timestamp is included independent of this text.
;exif_text %i%J/%K%L

############################################################
# Target Directories and filenames For Images And Films
# For the options snapshot_, picture_, movie_ and timelapse_filename
# you can use conversion specifiers
# %Y = year, %m = month, %d = date,
# %H = hour, %M = minute, %S = second,
# %v = event, %q = frame number, %t = camera id number,
# %D = changed pixels, %N = noise level,
# %i and %J = width and height of motion area,
# %K and %L = X and Y coordinates of motion center
# %C = value defined by text_event
# Quotation marks round string are allowed.
############################################################

# Target base directory for pictures and films
# Recommended to use absolute path. (Default: current working directory)
target_dir /home/pi/PARKED

# File path for snapshots (jpeg or ppm) relative to target_dir
# Default: %v-%Y%m%d%H%M%S-snapshot
# Default value is equivalent to legacy oldlayout option
# For Motion 3.0 compatible mode choose: %Y/%m/%d/%H/%M/%S-snapshot
# File extension .jpg or .ppm is automatically added so do not include this.
# Note: A symbolic link called lastsnap.jpg created in the target_dir will always
# point to the latest snapshot, unless snapshot_filename is exactly 'lastsnap'
snapshot_filename %v--%Y-%m-%d-%H:%M:%S-snapshot

# File path for motion triggered images (jpeg or ppm) relative to target_dir
# Default: %v-%Y%m%d%H%M%S-%q
# Default value is equivalent to legacy oldlayout option
# For Motion 3.0 compatible mode choose: %Y/%m/%d/%H/%M/%S-%q
# File extension .jpg or .ppm is automatically added so do not include this
# Set to 'preview' together with best-preview feature enables special naming
# convention for preview shots. See motion guide for details
picture_filename %v--%Y-%m-%d-%H:%M:%S-%q

# File path for motion triggered ffmpeg films (movies) relative to target_dir
# Default: %v-%Y%m%d%H%M%S
# File extensions(.mpg .avi) are automatically added so do not include them
movie_filename %v--%Y-%m-%d-%H:%M:%S

# File path for timelapse movies relative to target_dir
# Default: %Y%m%d-timelapse
# File extensions(.mpg .avi) are automatically added so do not include them
timelapse_filename %Y%m%d-timelapse

############################################################
# Global Network Options
############################################################
# Enable IPv6 (default: off)
ipv6_enabled off

############################################################
# Live Stream Server
############################################################

# The mini-http server listens to this port for requests (default: 0 = disabled)
stream_port 9081

# Quality of the jpeg (in percent) images produced (default: 50)
stream_quality 50

# Output frames at 1 fps when no motion is detected and increase to the
# rate given by stream_maxrate when motion is detected (default: off)
stream_motion off

# Maximum framerate for stream streams (default: 1)
stream_maxrate 60

# Restrict stream connections to localhost only (default: on)
stream_localhost off

# Limits the number of images per connection (default: 0 = unlimited)
# Number can be defined by multiplying actual stream rate by desired number of seconds
# Actual stream rate is the smallest of the numbers framerate and stream_maxrate
stream_limit 0

# Set the authentication method (default: 0)
# 0 = disabled
# 1 = Basic authentication
# 2 = MD5 digest (the safer authentication)
stream_auth_method 1

# Authentication for the stream. Syntax username:password
# Default: not defined (Disabled)
stream_authentication pi:raspberry

# Percentage to scale the stream image for preview
# Default: 25
; stream_preview_scale 25

# Have stream preview image start on a new line
# Default: no
; stream_preview_newline no

############################################################
# HTTP Based Control
############################################################

# TCP/IP port for the http server to listen on (default: 0 = disabled)
webcontrol_port 0
#Recommended webcontrol_port 9080

# Restrict control connections to localhost only (default: on)
webcontrol_localhost off

# Output for http server, select off to choose raw text plain (default: on)
webcontrol_html_output on

# Authentication for the http based control. Syntax username:password
# Default: not defined (Disabled)
#
# (!) TODO - change the line below!
#
webcontrol_authentication user:password

############################################################
# Tracking (Pan/Tilt)
#############################################################

# Type of tracker (0=none (default), 1=stepper, 2=iomojo, 3=pwc, 4=generic, 5=uvcvideo, 6=servo)
# The generic type enables the definition of motion center and motion size to
# be used with the conversion specifiers for options like on_motion_detected
track_type 0

# Enable auto tracking (default: off)
track_auto off

# Serial port of motor (default: none)
;track_port /dev/ttyS0

# Motor number for x-axis (default: 0)
;track_motorx 0

# Set motorx reverse (default: 0)
;track_motorx_reverse 0

# Motor number for y-axis (default: 0)
;track_motory 1

# Set motory reverse (default: 0)
;track_motory_reverse 0

# Maximum value on x-axis (default: 0)
;track_maxx 200

# Minimum value on x-axis (default: 0)
;track_minx 50

# Maximum value on y-axis (default: 0)
;track_maxy 200

# Minimum value on y-axis (default: 0)
;track_miny 50

# Center value on x-axis (default: 0)
;track_homex 128

# Center value on y-axis (default: 0)
;track_homey 128

# ID of an iomojo camera if used (default: 0)
track_iomojo_id 0

# Angle in degrees the camera moves per step on the X-axis
# with auto-track (default: 10)
# Currently only used with pwc type cameras
track_step_angle_x 10

# Angle in degrees the camera moves per step on the Y-axis
# with auto-track (default: 10)
# Currently only used with pwc type cameras
track_step_angle_y 10

# Delay to wait for after tracking movement as number
# of picture frames (default: 10)
track_move_wait 10

# Speed to set the motor to (stepper motor option) (default: 255)
track_speed 255

# Number of steps to make (stepper motor option) (default: 40)
track_stepsize 40


############################################################
# External Commands, Warnings and Logging:
# You can use conversion specifiers for the on_xxxx commands
# %Y = year, %m = month, %d = date,
# %H = hour, %M = minute, %S = second,
# %v = event, %q = frame number, %t = camera id number,
# %D = changed pixels, %N = noise level,
# %i and %J = width and height of motion area,
# %K and %L = X and Y coordinates of motion center
# %C = value defined by text_event
# %f = filename with full path
# %n = number indicating filetype
# Both %f and %n are only defined for on_picture_save,
# on_movie_start and on_movie_end
# Quotation marks round string are allowed.
############################################################

# Do not sound beeps when detecting motion (default: on)
# Note: Motion never beeps when running in daemon mode.
quiet on

# Command to be executed when an event starts. (default: none)
# An event starts at first motion detected after a period of no motion defined by event_gap
;on_event_start python3 ~/.motion/motionalert.py

# Command to be executed when an event ends after a period of no motion
# (default: none). The period of no motion is defined by option event_gap.
;on_event_end value

# Command to be executed when a picture (.ppm|.jpg) is saved (default: none)
# To give the filename as an argument to a command append it with %f
#
# TODO: change the email below
#
on_picture_save mpack -s "Camera has detected Motion!" %f YourEmail@gmail.com

# Command to be executed when a motion frame is detected (default: none)
;on_motion_detected python3 ~/.motion/motionalert.py

# Command to be executed when motion in a predefined area is detected
# Check option 'area_detect'.   (default: none)
# 
; on_area_detected

# Command to be executed when a movie file (.mpg|.avi) is created. (default: none)
# To give the filename as an argument to a command append it with %f
; on_movie_start value

# Command to be executed when a movie file (.mpg|.avi) is closed. (default: none)
# To give the filename as an argument to a command append it with %f
;on_movie_end python3 ~/.motion/motionvid.py

# Command to be executed when a camera can't be opened or if it is lost
# NOTE: There is situations when motion don't detect a lost camera!
# It depends on the driver, some drivers dosn't detect a lost camera at all
# Some hangs the motion thread. Some even hangs the PC! (default: none)
; on_camera_lost value

#####################################################################
# Common Options for database features.
# Options require database options to be active also.
#####################################################################

# Log to the database when creating motion triggered picture file  (default: on)
; sql_log_picture on

# Log to the database when creating a snapshot image file (default: on)
; sql_log_snapshot on

# Log to the database when creating motion triggered movie file (default: off)
; sql_log_movie off

# Log to the database when creating timelapse movies file (default: off)
; sql_log_timelapse off

# SQL query string that is sent to the database
# Use same conversion specifiers has for text features
# Additional special conversion specifiers are
# %n = the number representing the file_type
# %f = filename with full path
# Default value:
# Create tables :
##
# Mysql
# CREATE TABLE security (camera int, filename char(80) not null, frame int, file_type int, time_stamp timestamp(14), event_time_stamp timestamp(14));
#
# Postgresql
# CREATE TABLE security (camera int, filename char(80) not null, frame int, file_type int, time_stamp timestamp without time zone, event_time_stamp timestamp without time zone);
#
# insert into security(camera, filename, frame, file_type, time_stamp, text_event) values('%t', '%f', '%q', '%n', '%Y-%m-%d %T', '%C')
; sql_query insert into security(camera, filename, frame, file_type, time_stamp, event_time_stamp) values('%t', '%f', '%q', '%n', '%Y-%m-%d %T', '%C')


############################################################
# Database Options
############################################################

# database type : mysql, postgresql, sqlite3 (default : not defined)
; database_type value

# database to log to (default: not defined)
# for sqlite3, the full path and name for the database.
; database_dbname value

# The host on which the database is located (default: localhost)
; database_host value

# User account name for database (default: not defined)
; database_user value

# User password for database (default: not defined)
; database_password value

# Port on which the database is located
#  mysql 3306 , postgresql 5432 (default: not defined)
; database_port value

# Database wait time in milliseconds for locked database to
# be unlocked before returning database locked error (default 0)
; database_busy_timeout 0



############################################################
# Video Loopback Device (vloopback project)
############################################################

# Output images to a video4linux loopback device
# The value '-' means next available (default: not defined)
; video_pipe value

# Output motion images to a video4linux loopback device
# The value '-' means next available (default: not defined)
; motion_video_pipe value


##############################################################
# camera config files - One for each camera.
# Except if only one camera - You only need this config file.
# If you have more than one camera you MUST define one camera
# config file for each camera in addition to this config file.
##############################################################

# Remember: If you have more than one camera you must have one
# camera file for each camera. E.g. 2 cameras requires 3 files:
# This motion.conf file AND camera1.conf and camera2.conf.
# Only put the options that are unique to each camera in the
# camera config files.
; camera /etc/motion/camera1.conf
; camera /etc/motion/camera2.conf
; camera /etc/motion/camera3.conf
; camera /etc/motion/camera4.conf


##############################################################
# Camera config directory - One for each camera.
##############################################################
#
; camera_dir /etc/motion/conf.d

"""

os.chdir('/etc/samba')

with open('smb.conf', 'a+') as f: #append smb to /etc/samba/smb.conf
  f.write(smb)
f.close()

os.system('sudo smbpasswd -a pi')
os.system('sudo systemctl restart smbd')

os.chdir('/etc/ssh')

with open('sshd_config', 'w+') as f: #write sshd_config to /etc/ssh/sshd_config
  f.write(sshd_config)
f.close()

os.system('sudo service ssh restart')

os.chdir('/home/pi/.motion')

with open('parked.conf', 'w+') as f: #write parked to ~/.motion/parked.conf
  f.write(parked)
f.close()

os.chdir('/etc/default')

with open('motion', 'w+') as f: #write daemon to /etc/default/motion
  f.write(daemon)
f.close()

os.chdir('/home/pi/BB_NETWORK')

#~/BB_NETWORK/network_init.sh
network_on = """\
#! /bin/bash

echo "[*]Shutting down other network processes..."
sudo airmon-ng check kill
echo "[*]Starting network..."
sudo nohup hostapd /home/pi/BB_NETWORK/hostapd.conf &
echo "[+]Network Running!"
"""

with open('network_init.sh', 'w+') as f:
  f.write(network_on)
f.close()

os.chdir('/etc/cron.d')

with open('network_init', 'w+') as f:
  f.write('@reboot bash /home/pi/BB_NETWORK/network_init.sh')
f.close()

os.chdir('/home/pi/.motion')

#~/.motion/parked.sh
parked_on = """\
#! /bin/bash

echo "[*]Starting motion daemon..."
sudo service motion start
echo "[*]Starting motion server..."
sudo motion -c ~/.motion/parked.conf
echo "[*]Starting snapshot server in /home/pi/PARKED on port 9082"
cd /home/pi/PARKED
nohup python ~/.motion/SecureHTTPServer.py 9082 'pi:raspberry' &
echo "[*]PARKED Mode Activated!"
"""

#~/.motion/driving.sh
driving_on = """\
~! /bin/bash

echo "[*]Starting motion daemon..."
sudo service motion start
echo "[*]Starting motion server..."
read -p "How long do you want to record?(10sec = 10000, 1min = 60000, 1hr = 3600000, 6h = 21600000): " time
sudo raspivid -o /home/pi/DRIVING/$(date +"%D-%R").h264 -t $time
echo "[*]Driving Mode Activated!"
echo "[*]To convert videos to .mp4 format use 'MP4Box -add video.h264 video.mp4'"
"""

#~/.motion/SecureHTTPServer.py
SecureHTTPServer = """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import base64
import BaseHTTPServer

from SimpleHTTPServer import SimpleHTTPRequestHandler


class AuthenticationHandler(SimpleHTTPRequestHandler):
    key = ''

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Secure HTTP Environment\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.getheader('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write('No auth received')
        elif self.headers.getheader('Authorization') == 'Basic ' + self.key:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('Not authenticated')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: SecureHTTPServer.py [port] [username:password]"
        sys.exit()
    AuthenticationHandler.key = base64.b64encode(sys.argv[2])
    BaseHTTPServer.test(AuthenticationHandler, BaseHTTPServer.HTTPServer)
"""

with open('driving.sh', 'w+') as f:
  f.write(driving_on)
f.close()

with open('parked.sh', 'w+') as f: #write arm to ~/.motion/parked.sh
  f.write(parked_on)
f.close()

with open('SecureHTTPServer.py', 'w+') as f: #write SecureHTTPServer to ~/.motion/SecureHTTPServer.py
  f.write(SecureHTTPServer)
f.close()

with open('/home/pi/.bashrc', 'a+') as f:
  f.write("alias BB_Dashcam_on='bash /home/pi/.motion/driving.sh'")
  f.write("alias BB_Dashcam_parked='bash /home/pi/.motion/parked.sh'")
  f.write("alias BB_Dashcam_off='sudo service motion stop && ps aux | grep python'")
  f.write("alias BB_Network_on='bash /home/pi/BB_NETWORK/network_init.sh'")
  f.write("alias BB_Network_off='sudo service hostapd stop'")
f.close()

print('[+]Setup Complete!')
print("[*]Camera controls: BB_Dashcam_on(Driving Mode), BB_Dashcam_parked, BB_Dashcam_off, BB_Network_on, BB_Network_off,  ")

